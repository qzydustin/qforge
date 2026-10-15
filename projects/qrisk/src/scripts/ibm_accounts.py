#!/usr/bin/env python3
"""
IBM Quantum account management utilities.

Commands:
    python -m scripts.ibm_accounts status
        List all accounts with remaining time.

    python -m scripts.ibm_accounts cancel
        Cancel all pending/queued jobs across all accounts (dry run).

    python -m scripts.ibm_accounts cancel --execute
        Actually cancel the jobs (not just preview).

    python -m scripts.ibm_accounts cancel --account "my-account"
        Cancel jobs for a specific account only.
"""

from __future__ import annotations

import argparse

from qrisk.config import load_config
from qrisk.ibm_runtime import cancel_jobs_for_account, list_account_remaining


def cmd_status(args):
    """List all accounts and their remaining time."""
    rows = list_account_remaining(load_config())
    if not rows:
        print("No accounts found.")
        return

    print(f"{'#':>2}  {'Account':<25}  {'Remaining':>8}  {'Backend':<15}  {'Error'}")
    print("-" * 75)
    for r in rows:
        mins = "-" if r["remaining_minutes"] is None else f"{r['remaining_minutes']:.1f}m"
        err = r.get("error") or ""
        print(f"{r['index']:>2}  {r['name']:<25}  {mins:>8}  {r['backend'] or '':.<15}  {err}")
    print()
    total = sum(r["remaining_seconds"] for r in rows if r.get("remaining_seconds"))
    print(f"Total: {total / 60:.1f} minutes across {len(rows)} accounts")


def cmd_cancel(args):
    """Cancel pending/queued jobs."""
    config = load_config()
    accounts = config["ibm_quantum"].get("accounts", [])
    if args.account:
        accounts = [a for a in accounts if a["name"] == args.account]
        if not accounts:
            print(f"Account '{args.account}' not found.")
            return

    dry_run = not args.execute
    if dry_run:
        print("DRY RUN — add --execute to actually cancel\n")

    total_cancelled = 0
    for acct in accounts:
        name = acct["name"]
        print(f"Account: {name}")
        try:
            results = cancel_jobs_for_account(config, acct, limit=50, dry_run=dry_run)
        except Exception as e:
            print(f"  Error: {e}\n")
            continue

        if not results:
            print("  No pending jobs.\n")
            continue

        for r in results:
            action = "CANCELLED" if r.get("cancel_called") else "would cancel"
            print(f"  {r['job_id']}  {r.get('status_before','?')} -> {action}")
        total_cancelled += len(results)
        print()

    print(f"Total: {total_cancelled} jobs {'cancelled' if args.execute else 'would be cancelled'}")


def main():
    parser = argparse.ArgumentParser(description="IBM Quantum account manager")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="List accounts and remaining time")

    cancel_p = sub.add_parser("cancel", help="Cancel pending jobs")
    cancel_p.add_argument("--execute", action="store_true", help="Actually cancel (default is dry run)")
    cancel_p.add_argument("--account", default=None, help="Specific account name")

    args = parser.parse_args()
    if args.command == "status":
        cmd_status(args)
    elif args.command == "cancel":
        cmd_cancel(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

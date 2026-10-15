#!/usr/bin/env python3
"""
Stable demo sample for mutation walking.

Design goals:
- Default execution prints exactly one numeric result (stable across runs).
- Optional, "semantically tempting" branches are gated behind environment flags.
- No randomness, no external I/O, no time-based logic.
- Safe defaults to reduce flaky runtime failures during smoke validation.

Environment flags (all default OFF):
- DEMO_ENABLE_FRAUD=1        Enable extra fraud logic (more branches).
- DEMO_ENABLE_LOYALTY=1      Enable loyalty/vip adjustments.
- DEMO_ENABLE_GEO=1          Enable geo/region parsing branches.
- DEMO_ENABLE_PROMO_DEBUG=1  Enable extra promotion debug branches.
- DEMO_VERBOSE=1             Print additional debug lines (off by default).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, List, Tuple


def _env_on(key: str) -> bool:
    value = os.environ.get(key, "").strip().lower()
    return value in {"1", "true", "yes", "y", "on"}


DEMO_ENABLE_FRAUD = _env_on("DEMO_ENABLE_FRAUD")
DEMO_ENABLE_LOYALTY = _env_on("DEMO_ENABLE_LOYALTY")
DEMO_ENABLE_GEO = _env_on("DEMO_ENABLE_GEO")
DEMO_ENABLE_PROMO_DEBUG = _env_on("DEMO_ENABLE_PROMO_DEBUG")
DEMO_VERBOSE = _env_on("DEMO_VERBOSE")


def _vprint(msg: str) -> None:
    if DEMO_VERBOSE:
        print(msg)


def clamp(value: float, lo: float, hi: float) -> float:
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value


def normalize_email(email: str) -> str:
    email_norm = (email or "").strip().lower()
    if "@" not in email_norm:
        email_norm = email_norm + "@example.com"
    email_norm = email_norm.replace(" ", "")
    if DEMO_ENABLE_GEO:
        if email_norm.endswith("@gmail.com"):
            email_norm = email_norm.replace("@gmail.com", "@googlemail.com")
    return email_norm


def parse_region(region: str) -> str:
    r = (region or "").strip().upper()
    if not r:
        return "US"
    if DEMO_ENABLE_GEO:
        if r in {"USA", "UNITEDSTATES", "UNITED_STATES"}:
            return "US"
        if r in {"CN", "CHN", "CHINA"}:
            return "CN"
        if r in {"EU", "EUR"}:
            return "EU"
    if r in {"US", "CA", "EU", "CN"}:
        return r
    return "US"


@dataclass(frozen=True)
class User:
    user_id: str
    email: str
    region: str
    vip: bool
    age: int


@dataclass(frozen=True)
class Item:
    sku: str
    price: float
    qty: int


def compute_subtotal(cart: List[Item]) -> float:
    total = 0.0
    for it in cart:
        q = it.qty if it.qty > 0 else 0
        p = it.price if it.price > 0 else 0.0
        total += p * float(q)
    return clamp(total, 0.0, 1_000_000.0)


def compute_tax(subtotal: float, region: str) -> float:
    r = parse_region(region)
    rate = 0.0
    if r == "US":
        rate = 0.0725
    elif r == "CA":
        rate = 0.13
    elif r == "EU":
        rate = 0.20
    elif r == "CN":
        rate = 0.09
    tax = subtotal * rate
    return clamp(tax, 0.0, 100_000.0)


def shipping_cost(subtotal: float, region: str) -> float:
    r = parse_region(region)
    base = 6.50
    if subtotal >= 50.0:
        base = 0.0
    if r in {"EU", "CN"}:
        base += 8.0
    if DEMO_ENABLE_GEO:
        if r == "CA":
            base += 1.25
    return clamp(base, 0.0, 1000.0)


def apply_promotions(
    subtotal: float,
    coupon: str,
    vip: bool = False,
    user: Dict[str, str] | None = None,
) -> float:
    code = (coupon or "").strip().upper()
    discount = 0.0

    if code == "SAVE10" and subtotal >= 20.0:
        discount += 0.10 * subtotal
    elif code == "FREESHIP":
        discount += 0.0
    elif code == "WELCOME5" and subtotal >= 10.0:
        discount += 5.0

    if DEMO_ENABLE_LOYALTY and vip:
        discount += min(12.0, 0.04 * subtotal)

    if DEMO_ENABLE_PROMO_DEBUG:
        if user and user.get("user_id", "").startswith("debug"):
            discount += 0.01 * subtotal

    discount = clamp(discount, 0.0, subtotal)
    return subtotal - discount


def fraud_risk_adjustment(user: User, subtotal: float) -> float:
    if not DEMO_ENABLE_FRAUD:
        return 0.0

    email_norm = normalize_email(user.email)
    score = 0.0

    if "@" not in email_norm:
        score += 0.40
    if user.age < 18:
        score += 0.25
    if subtotal > 500.0:
        score += 0.30

    domain = email_norm.split("@", 1)[-1]
    if domain.endswith(".ru"):
        score += 0.35
    if domain.endswith(".edu"):
        score -= 0.05

    score = clamp(score, 0.0, 1.0)
    return score


def score_checkout(
    user: User,
    cart: List[Item],
    coupon: str,
    vip: bool,
) -> Tuple[float, Dict[str, float]]:
    subtotal = compute_subtotal(cart)
    post_promo = apply_promotions(
        subtotal=subtotal,
        coupon=coupon,
        vip=vip,
        user={"user_id": user.user_id},
    )
    tax = compute_tax(post_promo, user.region)
    ship = shipping_cost(post_promo, user.region)

    fraud = fraud_risk_adjustment(user, post_promo)
    fraud_fee = 0.0
    if fraud >= 0.60:
        fraud_fee = 9.99
    elif fraud >= 0.30:
        fraud_fee = 2.49

    total = post_promo + tax + ship + fraud_fee
    total = clamp(total, 0.0, 1_000_000.0)

    details = {
        "subtotal": float(subtotal),
        "post_promo": float(post_promo),
        "tax": float(tax),
        "shipping": float(ship),
        "fraud": float(fraud),
        "fraud_fee": float(fraud_fee),
        "total": float(total),
    }
    return total, details


def score_user(user: User) -> float:
    email_norm = normalize_email(user.email)
    base = 50.0
    if user.vip:
        base += 15.0
    if user.age >= 30:
        base += 3.0
    if email_norm.endswith("@example.com"):
        base -= 2.0

    if DEMO_ENABLE_GEO:
        r = parse_region(user.region)
        if r == "EU":
            base += 1.0
        elif r == "CN":
            base -= 1.0

    return clamp(base, 0.0, 100.0)


def demo_run() -> float:
    user = User(
        user_id="u_1001",
        email="Test.User+tag@Example.com",
        region="US",
        vip=False,
        age=29,
    )

    cart = [
        Item(sku="A100", price=12.50, qty=2),
        Item(sku="B200", price=7.25, qty=1),
        Item(sku="C300", price=3.99, qty=3),
    ]

    coupon = "WELCOME5"
    vip = user.vip if DEMO_ENABLE_LOYALTY else False

    total, details = score_checkout(user=user, cart=cart, coupon=coupon, vip=vip)
    user_score = score_user(user)

    _vprint(f"details={details}")
    _vprint(f"user_score={user_score}")

    numeric_result = total + (user_score / 100.0)
    numeric_result = round(numeric_result, 6)
    return numeric_result


def main() -> None:
    result = demo_run()
    print(result)


if __name__ == "__main__":
    main()
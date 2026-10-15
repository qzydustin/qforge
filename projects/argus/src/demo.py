"""
demo_semantic_vs_random_light.py

Comparison:
- Baseline: random mutation (use_semantic_strategy = False)
- Smart   : semantic / coverage–aware mutation
            (use_semantic_strategy = True, use_coverage_strategy = True)

On the same source file, we perform N_TRIALS mutations for each strategy
and count how many mutants are “valid”.

Here a “valid mutant” uses a relaxed definition:
    - passes syntax check
    - can be executed within a timeout

We intentionally do NOT require a strict semantic check here.
"""

from pathlib import Path
from typing import Tuple

import matplotlib.pyplot as plt  # for bar chart

from random_mutator import mutate_code, CodeValidator  # Make sure this import matches your project structure


# ---------------------------
# Light-weight validation: syntax + execution only
# ---------------------------

def validate_code_light(code: str) -> Tuple[bool, str]:
    """
    Perform a relaxed validity check using CodeValidator:

      1) Syntax check
      2) Execution check

    We do **not** run a strict semantic check here. This makes it easier
    to see the difference between baseline and smart strategies in terms
    of “runnable mutants”.

    Returns:
        (is_valid, reason_if_invalid)
    """
    # 1) Syntax
    ok, err = CodeValidator.validate_syntax(code)
    if not ok:
        return False, f"syntax: {err}"

    # 2) Execution (usually import + a small run, depending on your implementation)
    ok, exec_err = CodeValidator.validate_execution(code, timeout=2)
    if not ok:
        return False, f"execution: {exec_err}"

    return True, ""


# ---------------------------
# Main experiment
# ---------------------------

def main():
    # ===== 1. Choose source file to mutate =====
    preferred = Path("examples") / "order_risk_pipeline.py"
    if preferred.exists():
        target_file = preferred
    else:
        candidate = Path("examples") / "score_user.py"
        if candidate.exists():
            target_file = candidate
        else:
            examples_dir = Path("examples")
            py_files = list(examples_dir.rglob("*.py"))
            if not py_files:
                raise FileNotFoundError("No .py files found under 'examples/'")
            target_file = py_files[0]

    print(f"[INFO] Using source file: {target_file}")
    src = target_file.read_text(encoding="utf-8")

    # Check original source under the light validation
    print("\n[DEBUG] Check original source validity (light validation):")
    ok0, reason0 = validate_code_light(src)
    print(f"Original valid? {ok0} | reason: {reason0}")

    # ===== 2. Experiment parameters =====
    N_TRIALS = 200   # Number of mutations per strategy
    STEPS = 3        # Number of mutation operators per run

    baseline_valid = 0
    smart_valid = 0

    # Fake coverage data so that smart mutation can use use_coverage_strategy
    fake_coverage = {"executed_lines": set(range(1, 2000))}

    priority_dependencies = [
        "total_amount",
        "refund_rate",
        "vip_level",
        "risk_flags",
        "compute_risk_score",
        "decide_action",
    ]

    # ===== 3. Baseline: no semantic / coverage strategies =====
    print("\n=== Baseline: random mutation (no semantic / coverage strategy) ===")
    for k in range(N_TRIALS):
        try:
            mutated, history = mutate_code(
                source_code=src,
                steps=STEPS,
                seed=1000 + k,        # for reproducibility
                custom_operators=None,
                validate=False,       # we apply validate_code_light externally
                use_coverage_strategy=False,
                use_semantic_strategy=False,   # semantic strategy OFF
                coverage_data=None,
                priority_dependencies=None,
            )
            ok, reason = validate_code_light(mutated)
            if ok:
                baseline_valid += 1
        except Exception:
            # treat mutation failures as invalid mutants
            pass

    # ===== 4. Smart: enable semantic + coverage strategies =====
    print("\n=== Smart: semantic + coverage-aware mutation ===")
    for k in range(N_TRIALS):
        try:
            mutated, history = mutate_code(
                source_code=src,
                steps=STEPS,
                seed=2000 + k,        # different seed range
                custom_operators=None,
                validate=True,        # internal checks if you want
                use_coverage_strategy=True,
                use_semantic_strategy=True,    # semantic strategy ON
                coverage_data=fake_coverage,
                priority_dependencies=priority_dependencies,
            )
            ok, reason = validate_code_light(mutated)
            if ok:
                smart_valid += 1
        except Exception:
            pass

    # ===== 5. Print comparison result =====
    baseline_ratio = baseline_valid / N_TRIALS
    smart_ratio = smart_valid / N_TRIALS

    print(f"\n=== Summary: Valid Mutant Comparison ({N_TRIALS} trials each) ===")
    print(
        f"Baseline (no semantic / coverage): "
        f"{baseline_valid}/{N_TRIALS} "
        f"({baseline_ratio:.2%}) valid mutants"
    )
    print(
        f"Smart    (semantic+coverage on): "
        f"{smart_valid}/{N_TRIALS} "
        f"({smart_ratio:.2%}) valid mutants"
    )

    # ===== 6. Plot bar chart =====
    labels = ["Baseline", "Smart"]
    values = [baseline_ratio * 100, smart_ratio * 100]  # convert to percentage

    plt.figure()
    plt.bar(labels, values)
    plt.ylabel("Valid mutant ratio (%)")
    plt.title("Baseline vs Smart Mutation (valid mutants)")

    # Optionally annotate bars with exact percentages
    for i, v in enumerate(values):
        plt.text(i, v + 1, f"{v:.1f}%", ha="center")

    plt.tight_layout()
    plt.savefig("valid_mutant_comparison.png", dpi=200)
    # If you want the window to pop up when running locally, uncomment:
    # plt.show()

    print("\n→ Bar chart saved as 'valid_mutant_comparison.png'.")
    print("   You can insert this image directly into your slide.")


if __name__ == "__main__":
    main()
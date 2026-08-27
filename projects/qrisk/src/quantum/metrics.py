from typing import Dict, Tuple


def calculate_tvd(counts_a: Dict[str, int], counts_b: Dict[str, int]) -> Tuple[float, Dict[str, dict]]:
    """Calculate Total Variation Distance between two count distributions.

    TVD = 0.5 * sum(|p_a(x) - p_b(x)|) for all states x.
    Returns a value in [0, 1]: 0 = identical, 1 = completely disjoint.
    """
    total_a = sum((counts_a or {}).values())
    total_b = sum((counts_b or {}).values())

    if total_a == 0 or total_b == 0:
        return 0.0, {}

    all_states = set(counts_a) | set(counts_b)
    tvd = 0.0
    state_details: Dict[str, dict] = {}

    for state in sorted(all_states):
        prob_a = counts_a.get(state, 0) / total_a
        prob_b = counts_b.get(state, 0) / total_b
        diff = abs(prob_a - prob_b)
        tvd += diff
        state_details[state] = {
            "prob_a": prob_a,
            "prob_b": prob_b,
            "abs_diff": diff,
            "count_a": counts_a.get(state, 0),
            "count_b": counts_b.get(state, 0),
        }

    tvd *= 0.5
    return tvd, state_details

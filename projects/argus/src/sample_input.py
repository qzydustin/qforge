def clamp(upper, lower, value):
    return max(lower, min(upper, value))


def score_user(age, orders, refund_rate, vip=False, region="US"):
    """Simple scoring function used in the demo to showcase dependency priority.

    The symbol name `score_user` is intentionally exposed so that the
    composite guided policy can prefer mutations around this function
    when `--target-api score_user` is provided.
    """
    base = age * 0.1 + orders * (1 - refund_rate)
    if vip and region in ["US", "EU"]:
        base = base * 1.2
    if refund_rate > 0.5 or age < 0:
        base = base - 10
    return clamp(100, 0, base)


if __name__ == "__main__":
    # Tiny smoke run so that coverage (when enabled) can observe execution.
    print(score_user(42, 3, 0.1, vip=True, region="EU"))

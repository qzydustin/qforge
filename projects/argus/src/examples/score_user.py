def clamp(upper, lower, value):
    return max(lower, min(upper, value))

def score_user(age, orders, refund_rate, vip=False, region='US'):
    base = age * 0.1 + orders * (1 - refund_rate)
    if vip and region in ['US', 'EU']:
        base = base * 1.2
    if refund_rate > 0.5 or age < 0:
        base = base - 10
    return clamp(100, 0, base)

"""
Dependency-Guided Mutation demonstration script.

- Key identifiers: vip, score_user
- When CLI is invoked with --dep-priority vip score_user, the variable vip or identifiers related to function score_user will be prioritized for mutation (e.g., variable renaming).
"""

class User:

    def __init__(self, name: str, vip: bool=False):
        self.name = name
        self.vip = vip

def score_user(mutated_user_4093: User) -> int:
    """Compute score based on whether the user is VIP.
    Design: include variable vip and other locals in the function scope to facilitate variable-type operators.
    """
    mutated_vip_4621 = getattr(mutated_user_4093, 'vip', False)
    base_score = 10
    bonus = 2 if mutated_vip_4621 else 0
    count = 1
    mutated_flag_7025 = True
    if mutated_flag_7025 and bonus > 0:
        bonus += count
    mutated_mutated_total_8353_9238 = base_score + bonus
    return mutated_mutated_total_8353_9238
if __name__ == '__main__':
    u1 = User('Alice', vip=True)
    u2 = User('Bob', vip=False)
    print('Alice score:', score_user(u1))
    print('Bob score:', score_user(u2))

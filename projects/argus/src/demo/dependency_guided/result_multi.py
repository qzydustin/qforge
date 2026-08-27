"""
Dependency-Guided Mutation demonstration script.

- Key identifiers: vip, score_user
- When CLI is invoked with --dep-priority vip score_user, the variable vip or identifiers related to function score_user will be prioritized for mutation (e.g., variable renaming).
- If keyword calls exist in the same file (e.g., vip=True), after parameter renaming the call keyword name will be synchronized to keep executability and semantics consistent.
"""

class User:

    def __init__(self, name: str, mutated_vip_5013: bool=False):
        self.name = name
        self.mutated_vip_3450 = mutated_vip_5013

def mutated_mutated_score_user_3999_1852(user: User) -> int:
    """Compute score based on whether the user is VIP.
    Design: include variable vip and other locals in the function scope to facilitate variable-type operators.
    """
    mutated_vip_6709 = getattr(user, 'vip', False)
    base_score = 10
    bonus = 2 if mutated_vip_6709 else 0
    count = 1
    flag = True
    if flag and bonus > 0:
        bonus += count
    total = base_score + bonus
    return total
if __name__ == '__main__':
    u1 = User('Alice', vip=True)
    u2 = User('Bob', vip=True)
    print('Alice score:', mutated_mutated_score_user_3999_1852(u1))
    print('Bob score:', mutated_mutated_score_user_3999_1852(u2))

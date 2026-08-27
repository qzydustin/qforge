# -*- coding: utf-8 -*-
"""
Dependency-Guided Mutation demonstration script.

- Key identifiers: vip, score_user
- When CLI is invoked with --dep-priority vip score_user, the variable vip or identifiers related to function score_user will be prioritized for mutation (e.g., variable renaming).
- If keyword calls exist in the same file (e.g., vip=True), after parameter renaming the call keyword name will be synchronized to keep executability and semantics consistent.
"""

class User:
    def __init__(self, name: str, vip: bool = False):
        self.name = name
        self.vip = vip


def score_user(user: User) -> int:
    """Compute score based on whether the user is VIP.
    Design: include variable vip and other locals in the function scope to facilitate variable-type operators.
    """
    # Local variable that can hit dependencies: vip
    vip = getattr(user, 'vip', False)

    # Other simple locals to provide multiple candidates for variable-type operators
    base_score = 10
    bonus = 2 if vip else 0
    count = 1
    flag = True

    if flag and bonus > 0:
        bonus += count

    total = base_score + bonus
    return total


if __name__ == '__main__':
    # Simple runnable example
    u1 = User('Alice', vip=True)
    u2 = User('Bob', vip=False)
    print('Alice score:', score_user(u1))
    print('Bob score:', score_user(u2))

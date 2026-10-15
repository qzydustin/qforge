# ===== sample_long.py =====
# This code is used for comprehensive testing of the mutation engine. It avoids external dependencies and I/O for easy execution in restricted environments.

# Simple utility functions
def clamp(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x

def mean(nums):
    total = 0
    count = 0
    for n in nums:
        total = total + n
        count = count + 1
    return total / count if count != 0 else 0.0

def median(nums):
    arr = list(nums)
    arr.sort()
    n = len(arr)
    if n == 0:
        return 0
    mid = n // 2
    if n % 2 == 1:
        return arr[mid]
    else:
        return (arr[mid - 1] + arr[mid]) / 2

def variance(nums):
    m = mean(nums)
    acc = 0.0
    for v in nums:
        d = v - m
        acc = acc + d * d
    return acc / (len(nums) or 1)

# Multi-parameter function (for parameter mutator)
def score_user(age, orders, refund_rate, vip=False, region="US"):
    base = age * 0.1 + orders * (1 - refund_rate)
    if vip and region in ("US", "EU"):
        base = base * 1.2
    if refund_rate > 0.5 or age < 0:
        base = base - 10
    return clamp(base, 0, 100)

# Algorithm: Fibonacci (mix of recursion + loop)
def fibonacci(n):
    if n <= 1:
        return n
    a = 0
    b = 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

def factorial(n):
    if n < 0:
        return 1
    res = 1
    i = 2
    while i <= n:
        res = res * i
        i = i + 1
    return res

# Search and sort
def binary_search(arr, target):
    lo = 0
    hi = len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

# Data structure playground: list/tuple/set/dict
def structure_playground(numbers):
    xs = list(numbers)
    ys = tuple(xs)
    zs = set(xs)
    m = {"sum": sum(xs), "min": min(xs) if xs else 0, "max": max(xs) if xs else 0}
    # Some removable/mutable expressions
    dummy = 0
    dummy = dummy + 1
    if len(zs) > 3 and (m["max"] > 10 or m["min"] < 0):
        xs.append(m["sum"])
    if True and False or (len(xs) > 2 and len(ys) >= 1):
        m["avg"] = mean(xs)
    else:
        m["avg"] = 0.0
    return xs, ys, zs, m

# Condition and boolean flipping playground
def quality_gate(score, flags):
    # flags is a dict, e.g., {"abuse": False, "fraud": True}
    passed = score >= 60 and not flags.get("abuse", False)
    if flags.get("fraud", False) or flags.get("spam", False):
        passed = False
    if (flags.get("whitelist", False) and score > 50) or (score > 80 and not flags.get("ban", False)):
        passed = True
    return passed

# Loop boundaries: range and while
def range_math(n):
    acc = 0
    for i in range(1, n):  # Note: boundaries can be mutated by ±1
        acc = acc + (i * 2 - i // 3)
    t = 0
    k = n
    while k > 0:
        t = t + k
        k = k - 1
    return acc + t

# Slightly more complex business class
class Ledger:
    def __init__(self):
        self.balance = 0
        self.history = []

    def deposit(self, amount, note=""):
        if amount <= 0:
            return False
        self.balance = self.balance + amount
        self.history.append(("in", amount, note))
        return True

    def withdraw(self, amount, note=""):
        if amount <= 0:
            return False
        if self.balance >= amount:
            self.balance = self.balance - amount
            self.history.append(("out", amount, note))
            return True
        else:
            return False

    def snapshot(self):
        # Return a tuple to facilitate structural mutations
        return (self.balance, tuple(self.history))

# Simple "transaction": prepare/commit/rollback (for condition, comparison, and deletion mutations)
def transfer(ledger_a, ledger_b, amount, allow_overdraft=False):
    # prepare
    ok_a = ledger_a.withdraw(amount, note="reserve")
    if not ok_a:
        if allow_overdraft and ledger_a.balance + amount > 0:
            ok_a = True
        else:
            return False

    # commit
    ok_b = ledger_b.deposit(amount, note="income")
    if not ok_b:
        # rollback
        ledger_a.deposit(amount, note="rollback")
        return False

    # validation
    if ledger_b.balance < 0 or ledger_a.balance < -1000:
        return False
    return True

# Playground for dict key/value swap and data structure changes
def invert_mapping(pairs):
    d = {k: v for k, v in pairs}  # dict
    # Introduce content that can be "key/value swapped" by the mutator
    if len(d) > 0 and (len(d) % 2 == 0 or len(d) > 3):
        # Pure logic, no side effects
        pass
    # Invert mapping (simple handling: values may duplicate)
    inv = {}
    for k, v in d.items():
        inv.setdefault(v, []).append(k)
    return d, inv

# Multi-parameter call composition, for parameter position swapping
def blended_compute(a, b, c, scale=1, bias=0):
    t1 = a + b * c
    t2 = factorial(scale) if scale > 0 else 1
    return t1 * t2 + bias

def pipeline(numbers):
    # Chained function calls (multi-parameter), for FunctionCallParameterMutator to play
    arr = list(numbers)
    arr2 = bubble_sort(arr)
    acc = range_math(len(arr2) + 3)
    sc = score_user(age=len(arr2) * 3, orders=int(mean(arr2) or 1), refund_rate=0.1, vip=True, region="EU")
    ok = quality_gate(sc, {"abuse": False, "fraud": False, "whitelist": True})
    x = blended_compute(acc, sc, len(arr2), scale=3, bias=5)
    return {"ok": ok, "score": sc, "val": x, "acc": acc, "n": len(arr2)}

# Main function
def main():
    nums = [5, 3, 9, 1, 7, 2, 8, 6, 4, 10]
    print("mean/median/var:", mean(nums), median(nums), round(variance(nums), 3))

    xs, ys, zs, m = structure_playground(nums)
    print("structures:", len(xs), len(ys), len(zs), m.get("avg", 0.0))

    print("fib(10)=", fibonacci(10), "fact(6)=", factorial(6))
    print("binsearch 7 @:", binary_search(bubble_sort(list(nums)), 7))

    la = Ledger()
    lb = Ledger()
    la.deposit(100, "init A")
    lb.deposit(50, "init B")
    print("transfer:", transfer(la, lb, 30), "balances:", la.balance, lb.balance)

    d, inv = invert_mapping([("a", 1), ("b", 2), ("c", 1), ("d", 3)])
    print("map sizes:", len(d), len(inv))

    res = pipeline([1, 2, 3, 4, 5])
    print("pipeline:", res)

# ===== end of sample_long.py =====

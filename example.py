"""
example.py
==========

A simple example showing how to use the fast_math C++ module.
Run this after installing with: pip install -e .

This is the simplest possible demonstration - no benchmarking,
just showing that you can call C++ functions from Python.
"""

# Import the C++ module (after building with pip install -e .)
import fast_math

print("=" * 50)
print("C++ Module Demo")
print("=" * 50)

# Example 1: Sum of squares
# -------------------------
n = 100
result = fast_math.sum_of_squares(n)
print(f"\nSum of squares from 1 to {n}:")
print(f"  1² + 2² + 3² + ... + {n}² = {result}")

# Example 2: Count primes
# -----------------------
n = 1000
count = fast_math.count_primes(n)
print(f"\nPrime numbers from 2 to {n}:")
print(f"  There are {count} primes")

# Example 3: Fibonacci
# --------------------
n = 20
fib = fast_math.fibonacci(n)
print(f"\nFibonacci number #{n}:")
print(f"  F({n}) = {fib}")

# Example 4: Array sum (passing a Python list to C++)
# ---------------------------------------------------
numbers = [1.5, 2.5, 3.5, 4.5, 5.0]
total = fast_math.array_sum(numbers)
print(f"\nSum of {numbers}:")
print(f"  Total = {total}")

# Getting help
# ------------
print("\n" + "=" * 50)
print("Getting help on the module:")
print("=" * 50)
print("\nAvailable functions:", [x for x in dir(fast_math) if not x.startswith('_')])
print("\nModule documentation:")
print(fast_math.__doc__)

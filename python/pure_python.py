"""
pure_python.py
==============

This file contains PURE PYTHON implementations of the same functions
we wrote in C++. By comparing execution times, you'll see exactly
why C++ is used for performance-critical code.

WHY IS PYTHON SLOWER?
---------------------
1. INTERPRETED vs COMPILED
   - Python: Each line is translated to machine code AS IT RUNS
   - C++: The entire program is optimized and compiled BEFORE it runs

2. DYNAMIC TYPING
   - Python: Must check the type of every variable at runtime
   - C++: Types are known at compile time, no runtime checks needed

3. MEMORY MANAGEMENT
   - Python: Uses reference counting and garbage collection (overhead)
   - C++: You control memory directly (or use smart pointers)

4. GLOBAL INTERPRETER LOCK (GIL)
   - Python: Only one thread can execute Python code at a time
   - C++: True parallel execution across threads

This doesn't mean Python is bad! Python excels at:
- Rapid development
- Readable, maintainable code
- Huge ecosystem of libraries
- Gluing together different systems

The smart approach: Write most code in Python, optimize bottlenecks in C++.
"""


def sum_of_squares(n: int) -> int:
    """
    Calculate sum of squares from 1 to n: 1^2 + 2^2 + ... + n^2

    This is a straightforward loop - simple to write in Python,
    but loops are where Python's interpreted nature hurts most.
    """
    result = 0
    for i in range(1, n + 1):
        result += i * i
    return result


def count_primes(n: int) -> int:
    """
    Count prime numbers from 2 to n.

    For each number, we check if it's divisible by any smaller number
    (up to its square root). This nested loop really shows the
    performance difference.
    """
    if n < 2:
        return 0

    count = 0
    for num in range(2, n + 1):
        is_prime = True
        # Only need to check up to square root of num
        i = 2
        while i * i <= num:
            if num % i == 0:
                is_prime = False
                break
            i += 1
        if is_prime:
            count += 1
    return count


def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number (iterative).

    We use iteration instead of recursion for fair comparison
    with the C++ version (both are O(n) algorithms).
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1

    prev2 = 0  # F(n-2)
    prev1 = 1  # F(n-1)

    for _ in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current

    return prev1


def array_sum(arr: list) -> float:
    """
    Sum all elements in a list.

    This demonstrates the data conversion overhead:
    - Python list -> C++ std::vector takes time
    - But the actual computation in C++ is still faster
    """
    total = 0.0
    for val in arr:
        total += val
    return total


# =============================================================================
# BONUS: "Pythonic" versions using built-in functions
# =============================================================================
# These use Python's built-in functions which are implemented in C!
# They're faster than pure Python loops but still not as fast as our C++.

def sum_of_squares_builtin(n: int) -> int:
    """Using sum() and generator expression - implemented in C internally."""
    return sum(i * i for i in range(1, n + 1))


def array_sum_builtin(arr: list) -> float:
    """Using built-in sum() - implemented in C internally."""
    return sum(arr)

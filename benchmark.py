"""
benchmark.py
============

This script compares the execution time of our C++ functions vs pure Python.
Run this AFTER installing the C++ module with: pip install -e .

USAGE
-----
    python benchmark.py

WHAT THIS SCRIPT DOES
---------------------
1. Imports both the C++ module (fast_math) and pure Python implementations
2. Runs each function with the same inputs
3. Measures execution time using time.perf_counter() (high precision timer)
4. Calculates the speedup ratio (Python time / C++ time)

EXPECTED RESULTS
----------------
You should see C++ being 10-100x faster depending on the operation.
The exact speedup depends on your CPU and the specific operation.
"""

import time
import sys

# Allow large integer string conversion
sys.set_int_max_str_digits(0)  # 0 = unlimited

# Import our pure Python implementations
from python.pure_python import (
    sum_of_squares as py_sum_of_squares,
    count_primes as py_count_primes,
    fibonacci as py_fibonacci,
    array_sum as py_array_sum,
)

# Try to import the C++ module
# If it fails, the user probably hasn't built it yet
try:
    import fast_math as cpp
except ImportError:
    print("=" * 60)
    print("ERROR: Could not import 'fast_math' module!")
    print("=" * 60)
    print()
    print("You need to build and install the C++ module first.")
    print("Run this command in your terminal:")
    print()
    print("    pip install -e .")
    print()
    print("If you get build errors, make sure you have:")
    print("  1. A C++ compiler installed (g++, clang++, or MSVC)")
    print("  2. pybind11 installed: pip install pybind11")
    print("=" * 60)
    sys.exit(1)


def benchmark(name: str, python_func, cpp_func, *args):
    """
    Run a benchmark comparing Python and C++ implementations.

    Parameters:
        name: Description of what we're benchmarking
        python_func: The pure Python function
        cpp_func: The C++ function (via pybind11)
        *args: Arguments to pass to both functions
    """
    print(f"\n{'=' * 60}")
    print(f"BENCHMARK: {name}")
    print(f"{'=' * 60}")

    # Benchmark Python
    start = time.perf_counter()
    py_result = python_func(*args)
    py_time = time.perf_counter() - start

    # Benchmark C++
    start = time.perf_counter()
    cpp_result = cpp_func(*args)
    cpp_time = time.perf_counter() - start

    # Verify results match (sanity check)
    if py_result != cpp_result:
        print(f"WARNING: Results don't match!")
        # For large numbers, just show digest instead of full number
        py_str = str(py_result)
        cpp_str = str(cpp_result)
        if len(py_str) > 50:
            py_display = f"{py_str[:25]}...{py_str[-25:]} ({len(py_str)} digits)"
        else:
            py_display = py_str
        if len(cpp_str) > 50:
            cpp_display = f"{cpp_str[:25]}...{cpp_str[-25:]} ({len(cpp_str)} digits)"
        else:
            cpp_display = cpp_str
        print(f"  Python: {py_display}")
        print(f"  C++:    {cpp_display}")
    else:
        result_str = str(cpp_result)
        if len(result_str) > 50:
            result_display = f"{result_str[:25]}...{result_str[-25:]} ({len(result_str)} digits)"
        else:
            result_display = result_str
        print(f"Result: {result_display}")

    # Display timing results
    print(f"\nPython time: {py_time:.6f} seconds")
    print(f"C++ time:    {cpp_time:.6f} seconds")

    # Calculate speedup
    if cpp_time > 0:
        speedup = py_time / cpp_time
        print(f"\nSpeedup: {speedup:.1f}x faster with C++")
    else:
        print("\nC++ time too small to measure accurately")

    return py_time, cpp_time


def main():
    print()
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print("*     C++ vs Python Performance Comparison                *")
    print("*" + " " * 58 + "*")
    print("*" * 60)

    # ==========================================================================
    # Benchmark 1: Sum of Squares
    # ==========================================================================
    n = 10_000_000  # 10 million
    benchmark(
        f"Sum of Squares (n={n:,})",
        py_sum_of_squares,
        cpp.sum_of_squares,
        n
    )

    # ==========================================================================
    # Benchmark 2: Prime Counting
    # ==========================================================================
    n = 100_000  # 100 thousand (this one is slow, so we use smaller n)
    benchmark(
        f"Count Primes up to {n:,}",
        py_count_primes,
        cpp.count_primes,
        n
    )

    # ==========================================================================
    # Benchmark 3: Fibonacci
    # ==========================================================================
    n = 1_000_000  # 1 million iterations
    benchmark(
        f"Fibonacci (n={n:,})",
        py_fibonacci,
        cpp.fibonacci,
        n
    )

    # ==========================================================================
    # Benchmark 4: Array Sum
    # ==========================================================================
    # Create a large list of numbers
    arr = list(range(1, 1_000_001))  # 1 million numbers
    benchmark(
        f"Array Sum ({len(arr):,} elements)",
        py_array_sum,
        cpp.array_sum,
        arr
    )

    # ==========================================================================
    # Summary
    # ==========================================================================
    print()
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print("*     KEY TAKEAWAYS                                       *")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    print("""
1. C++ is significantly faster for computational loops
2. The speedup is most dramatic for:
   - Nested loops (like prime counting)
   - Simple arithmetic operations
3. Array operations show less speedup because:
   - Data must be converted from Python list to C++ vector
   - This conversion has overhead that reduces the benefit
4. Use C++ for performance-critical code, Python for everything else!
""")


if __name__ == "__main__":
    main()

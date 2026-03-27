/*
 * math_operations.cpp
 * ===================
 *
 * This file contains pure C++ implementations of computationally intensive
 * functions. These functions will be exposed to Python using pybind11.
 *
 * WHY C++ FOR COMPUTATION?
 * ------------------------
 * Python is an interpreted language - each line is translated to machine code
 * at runtime. C++ is compiled - the entire program is translated to optimized
 * machine code BEFORE it runs. This makes C++ significantly faster for:
 *   - Loops with many iterations
 *   - Mathematical computations
 *   - Memory-intensive operations
 *
 * WHAT IS pybind11?
 * -----------------
 * pybind11 is a lightweight header-only library that lets you expose C++ code
 * to Python. Think of it as a "translator" that lets Python and C++ talk to
 * each other. It handles all the complex stuff like:
 *   - Converting Python types (list, int, float) to C++ types (vector, int, double)
 *   - Managing memory between the two languages
 *   - Creating a Python module from your C++ code
 */

#include <pybind11/pybind11.h>  // Core pybind11 functionality
#include <pybind11/stl.h>       // Automatic conversion for STL containers (vector, map, etc.)
#include <vector>
#include <cmath>

// Namespace alias - just a shorthand so we can write "py::" instead of "pybind11::"
namespace py = pybind11;


// =============================================================================
// FUNCTION 1: Sum of Squares
// =============================================================================
// Calculates: 1^2 + 2^2 + 3^2 + ... + n^2
//
// This is a simple example but with large n, the difference between
// Python and C++ becomes very noticeable.

long long sum_of_squares(long long n) {
    long long result = 0;
    for (long long i = 1; i <= n; ++i) {
        result += i * i;
    }
    return result;
}


// =============================================================================
// FUNCTION 2: Prime Counter
// =============================================================================
// Counts how many prime numbers exist between 2 and n.
//
// This is more computationally intensive because for each number,
// we need to check if it's divisible by any smaller number.

int count_primes(int n) {
    if (n < 2) return 0;

    int count = 0;
    for (int num = 2; num <= n; ++num) {
        bool is_prime = true;
        // Only need to check up to square root of num
        for (int i = 2; i * i <= num; ++i) {
            if (num % i == 0) {
                is_prime = false;
                break;  // Found a factor, no need to continue
            }
        }
        if (is_prime) {
            count++;
        }
    }
    return count;
}


// =============================================================================
// FUNCTION 3: Fibonacci (Iterative)
// =============================================================================
// Calculates the nth Fibonacci number.
//
// We use an iterative approach (not recursive) because:
// 1. It's faster - O(n) vs O(2^n) for naive recursion
// 2. It doesn't overflow the call stack for large n

long long fibonacci(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;

    long long prev2 = 0;  // F(n-2)
    long long prev1 = 1;  // F(n-1)
    long long current = 0;

    for (int i = 2; i <= n; ++i) {
        current = prev1 + prev2;
        prev2 = prev1;
        prev1 = current;
    }
    return current;
}


// =============================================================================
// FUNCTION 4: Array Sum (with std::vector)
// =============================================================================
// Sums all elements in a list/array.
//
// This demonstrates how pybind11 automatically converts:
//   Python list -> C++ std::vector
//
// The #include <pybind11/stl.h> at the top enables this conversion.

double array_sum(const std::vector<double>& arr) {
    double total = 0.0;
    for (const auto& val : arr) {
        total += val;
    }
    return total;
}


// =============================================================================
// PYBIND11 MODULE DEFINITION
// =============================================================================
// This is where the magic happens! This block tells pybind11:
// 1. What to name the Python module ("fast_math")
// 2. Which C++ functions to expose to Python
// 3. Documentation for each function
//
// PYBIND11_MODULE(module_name, module_variable)
//   - module_name: What you'll use in Python: "import fast_math"
//   - module_variable: A variable (m) we use to add functions to the module

PYBIND11_MODULE(fast_math, m) {
    // Module-level docstring (shows up when you do help(fast_math) in Python)
    m.doc() = "A fast math library written in C++ for Python";

    // Expose each function to Python
    // m.def("python_name", &cpp_function, "description")
    //   - "python_name": The name you'll use in Python
    //   - &cpp_function: Reference to the C++ function
    //   - "description": Docstring for help()

    m.def("sum_of_squares", &sum_of_squares,
          "Calculate sum of squares from 1 to n: 1^2 + 2^2 + ... + n^2");

    m.def("count_primes", &count_primes,
          "Count prime numbers from 2 to n");

    m.def("fibonacci", &fibonacci,
          "Calculate the nth Fibonacci number (iterative)");

    m.def("array_sum", &array_sum,
          "Sum all elements in a list/array");
}

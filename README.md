# C++ Python Integration Tutorial

A hands-on tutorial that teaches you how to integrate C++ code with Python using **pybind11**. This project demonstrates the performance benefits of using C++ for computationally intensive operations while keeping the ease of Python for everything else.

## Table of Contents

1. [Why Integrate C++ with Python?](#why-integrate-c-with-python)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Quick Start](#quick-start)
5. [Understanding the Code](#understanding-the-code)
6. [How pybind11 Works](#how-pybind11-works)
7. [The Build Process Explained](#the-build-process-explained)
8. [Using Your C++ Module in Python](#using-your-c-module-in-python)
9. [Troubleshooting](#troubleshooting)
10. [Next Steps](#next-steps)

---

## Why Integrate C++ with Python?

Python is fantastic for:
- Rapid development and prototyping
- Readable, maintainable code
- A massive ecosystem of libraries
- Data science, web development, scripting

But Python has limitations:
- **It's interpreted** - code is translated to machine instructions at runtime
- **Dynamic typing** - type checks happen every operation
- **The GIL** - only one thread executes Python code at a time

C++ excels where Python struggles:
- **Compiled** - code is optimized before it runs
- **Static typing** - no runtime type checks
- **True parallelism** - threads can run simultaneously
- **Manual memory control** - no garbage collection overhead

**The smart approach**: Write 95% of your code in Python, optimize the 5% that actually needs speed in C++.

---

## Prerequisites

Before you begin, you need:

### 1. Python 3.7+ with pip
Check with:
```bash
python --version
pip --version
```

### 2. A C++ Compiler

**Windows (Choose ONE):**
- **Visual Studio Build Tools** (Recommended)
  - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
  - During installation, select "Desktop development with C++"
- **MinGW-w64**
  - Download from: https://www.mingw-w64.org/

**macOS:**
```bash
xcode-select --install
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install build-essential
```

### 3. pybind11
```bash
pip install pybind11
```

---

## Project Structure

```
cpp-python-integration/
├── src/
│   └── math_operations.cpp    # C++ implementation + pybind11 bindings
├── python/
│   └── pure_python.py         # Pure Python implementation for comparison
├── benchmark.py               # Performance comparison script
├── setup.py                   # Build configuration (traditional)
├── pyproject.toml             # Build configuration (modern)
└── README.md                  # This file
```

### File Descriptions

| File | Purpose |
|------|---------|
| [src/math_operations.cpp](src/math_operations.cpp) | Contains C++ functions AND the pybind11 bindings that expose them to Python |
| [python/pure_python.py](python/pure_python.py) | Same functions written in pure Python for speed comparison |
| [benchmark.py](benchmark.py) | Runs both versions and measures the performance difference |
| [setup.py](setup.py) | Tells pip how to compile and install the C++ code |
| [pyproject.toml](pyproject.toml) | Modern build system configuration |

---

## Quick Start

### Step 1: Install the C++ Module

```bash
# Navigate to the project directory
cd path/to/this/project

# Install in "editable" mode (recommended for development)
pip install -e .
```

This command:
1. Reads `pyproject.toml` to install build dependencies (pybind11)
2. Runs `setup.py` to compile the C++ code
3. Creates `fast_math.pyd` (Windows) or `fast_math.so` (Linux/Mac)
4. Links it so Python can import it

### Step 2: Run the Benchmark

```bash
python benchmark.py
```

You should see output like:
```
************************************************************
*     C++ vs Python Performance Comparison                *
************************************************************

============================================================
BENCHMARK: Sum of Squares (n=10,000,000)
============================================================
Result: 333333283333335000000
Python time: 0.892341 seconds
C++ time:    0.012453 seconds

Speedup: 71.7x faster with C++
```

### Step 3: Use in Your Own Code

```python
import fast_math

# Call C++ functions just like Python functions!
result = fast_math.sum_of_squares(1000000)
primes = fast_math.count_primes(10000)
fib = fast_math.fibonacci(50)
```

---

## Understanding the Code

### The C++ File ([src/math_operations.cpp](src/math_operations.cpp))

This file has two parts:

#### Part 1: Pure C++ Functions
```cpp
long long sum_of_squares(long long n) {
    long long result = 0;
    for (long long i = 1; i <= n; ++i) {
        result += i * i;
    }
    return result;
}
```
These are normal C++ functions - nothing special about them.

#### Part 2: pybind11 Module Definition
```cpp
PYBIND11_MODULE(fast_math, m) {
    m.doc() = "A fast math library written in C++ for Python";

    m.def("sum_of_squares", &sum_of_squares,
          "Calculate sum of squares from 1 to n");
}
```
This tells pybind11:
- Create a Python module named `fast_math`
- Expose the C++ function `sum_of_squares` to Python
- Use the same name in Python as in C++

### The Pure Python File ([python/pure_python.py](python/pure_python.py))

Contains identical logic implemented in pure Python:
```python
def sum_of_squares(n: int) -> int:
    result = 0
    for i in range(1, n + 1):
        result += i * i
    return result
```

This lets us directly compare the performance of Python vs C++.

---

## How pybind11 Works

pybind11 is a **header-only** C++ library that creates a bridge between C++ and Python. Here's what happens:

### 1. Type Conversion
pybind11 automatically converts between Python and C++ types:

| Python Type | C++ Type |
|-------------|----------|
| `int` | `int`, `long`, `long long` |
| `float` | `float`, `double` |
| `str` | `std::string` |
| `list` | `std::vector<T>` |
| `dict` | `std::map<K, V>` |
| `None` | `nullptr` |

### 2. The Module Definition Macro

```cpp
PYBIND11_MODULE(module_name, m) {
    // 'm' is a pybind11::module_ object
    // Use it to add functions, classes, constants, etc.
}
```

- `module_name`: What you'll type in Python (`import module_name`)
- `m`: A variable representing the module; use it to add things

### 3. Exposing Functions

```cpp
m.def("python_name", &cpp_function, "docstring");
```

- `"python_name"`: The name to use in Python
- `&cpp_function`: Pointer to the C++ function
- `"docstring"`: Documentation (shows in `help()`)

---

## The Build Process Explained

When you run `pip install -e .`, here's what happens:

### Step 1: pip Reads pyproject.toml
```toml
[build-system]
requires = ["setuptools>=45", "pybind11>=2.10.0"]
```
pip installs these dependencies first.

### Step 2: pip Runs setup.py
```python
ext_modules = [
    Pybind11Extension(
        "fast_math",                    # Module name
        ["src/math_operations.cpp"],    # Source files
        extra_compile_args=["-O3"],     # Optimization flags
    ),
]
```

### Step 3: C++ Compiler Runs
The compiler:
1. Reads your `.cpp` file
2. Finds pybind11 headers
3. Compiles everything into a shared library

### Step 4: Shared Library Created
- **Windows**: `fast_math.cp311-win_amd64.pyd`
- **Linux**: `fast_math.cpython-311-x86_64-linux-gnu.so`
- **macOS**: `fast_math.cpython-311-darwin.so`

This file IS your Python module!

---

## Using Your C++ Module in Python

Once installed, use it like any Python module:

```python
# Import the module
import fast_math

# Check available functions
print(dir(fast_math))
# Output: ['__doc__', '__file__', ..., 'array_sum', 'count_primes', 'fibonacci', 'sum_of_squares']

# Get documentation
help(fast_math.sum_of_squares)
# Output: sum_of_squares(...) -- Calculate sum of squares from 1 to n

# Call functions
result = fast_math.sum_of_squares(1000000)
print(result)  # 333333833333500000

# Works with Python lists too!
numbers = [1.0, 2.0, 3.0, 4.0, 5.0]
total = fast_math.array_sum(numbers)
print(total)  # 15.0
```

### Example: Using in a Real Project

```python
import fast_math
import numpy as np

def process_data(data):
    """Process data using C++ for the heavy lifting."""

    # Python handles the high-level logic
    if not data:
        return None

    # C++ handles the computation
    total = fast_math.array_sum(data)

    return total / len(data)

# Use it
data = list(range(1, 10000001))  # 10 million numbers
average = process_data(data)
print(f"Average: {average}")
```

---

## Troubleshooting

### "Cannot find pybind11"

```bash
pip install pybind11
# Then retry:
pip install -e .
```

### "No C++ compiler found" (Windows)

Install Visual Studio Build Tools:
1. Download from https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Run the installer
3. Select "Desktop development with C++"
4. Restart your terminal

### "ImportError: DLL load failed"

This usually means the C++ runtime isn't installed. On Windows:
1. Download "Visual C++ Redistributable" from Microsoft
2. Install and restart

### Build Succeeds but Import Fails

Make sure you're in the right Python environment:
```bash
# Check which Python
python -c "import sys; print(sys.executable)"

# Reinstall
pip uninstall fast_math
pip install -e .
```

---

## Next Steps

Now that you understand the basics, here are some ways to expand your knowledge:

### 1. Add More Functions
Edit [src/math_operations.cpp](src/math_operations.cpp) and add your own functions!

### 2. Learn About Classes
pybind11 can expose C++ classes to Python:
```cpp
class Calculator {
public:
    int add(int a, int b) { return a + b; }
};

PYBIND11_MODULE(mymodule, m) {
    py::class_<Calculator>(m, "Calculator")
        .def(py::init<>())
        .def("add", &Calculator::add);
}
```

### 3. Explore NumPy Integration
pybind11 works great with NumPy:
```cpp
#include <pybind11/numpy.h>

double sum_numpy(py::array_t<double> arr) {
    auto buf = arr.request();
    double* ptr = static_cast<double*>(buf.ptr);
    double sum = 0;
    for (size_t i = 0; i < buf.size; i++)
        sum += ptr[i];
    return sum;
}
```

### 4. Read the pybind11 Documentation
https://pybind11.readthedocs.io/

---

## License

This is a learning project - feel free to use, modify, and share!

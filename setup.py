"""
setup.py
========

This file tells Python how to build and install your C++ extension module.
Think of it as a "recipe" that pip follows to create a usable Python package.

WHAT IS setup.py?
-----------------
In Python packaging, setup.py is the traditional way to configure how your
package should be built and installed. For C++ extensions, it also specifies:
  - Where to find the C++ source files
  - What compiler flags to use
  - What libraries to link against

WHAT IS pybind11?
-----------------
pybind11 provides a special "Extension" class that knows how to:
  1. Find the pybind11 headers (required for compilation)
  2. Set up the correct compiler flags for your platform
  3. Create a Python-importable module from your C++ code

HOW TO USE THIS FILE
--------------------
After creating this file, run ONE of these commands in your terminal:

  pip install .         # Install normally (copies to site-packages)
  pip install -e .      # "Editable" install (links to your source directory)
                        # Use -e during development so changes are reflected

The -e flag is super useful during development because you don't need to
reinstall every time you change the Python code. However, C++ changes
still require rebuilding: pip install -e . --force-reinstall
"""

from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext

# Define the C++ extension module
# ================================
# Pybind11Extension is a special class that sets up everything needed
# to compile C++ code with pybind11 bindings.

ext_modules = [
    Pybind11Extension(
        # Name of the module - this is what you'll import in Python
        # "import fast_math" will work after installation
        "fast_math",

        # List of C++ source files to compile
        # You can add more .cpp files here if your project grows
        ["src/math_operations.cpp"],

        # Optional: Extra compiler flags for optimization
        # -O3: Maximum optimization level (makes code faster)
        # You can add more flags here if needed
        extra_compile_args=["-O3"],
    ),
]

# Package configuration
# =====================
setup(
    # Package metadata
    name="fast_math",                           # Name on PyPI (if you publish)
    version="1.0.0",                            # Version number
    author="Your Name",                         # Your name
    description="A demo C++/Python integration project",

    # Build configuration
    ext_modules=ext_modules,                    # Our C++ extension(s)
    cmdclass={"build_ext": build_ext},          # Use pybind11's build command

    # Dependencies - pybind11 is needed to build this package
    install_requires=["pybind11>=2.10.0"],

    # This ensures pybind11 is available during the build process
    setup_requires=["pybind11>=2.10.0"],

    # Python version requirement
    python_requires=">=3.7",
)

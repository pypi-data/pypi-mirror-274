from setuptools import setup,find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "Complex_Bidintha",
    version="0.5",
    packages=find_packages(),
    author="Bidintha Machahry",
    author_email="bidintha2006@gmail.com",
    description="Complex Numbers",
    license="License.txt",
    url="https://github.com/MrS0lver/Complex_Number",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
#     long_description="""
# The ComplexNumbers package provides a simple implementation of complex numbers in Python. The package includes a Complex class with support for basic arithmetic operations such as addition, subtraction, multiplication, and division of complex numbers. Additionally, the class provides methods for calculating the absolute value (magnitude) of a complex number and comparing complex numbers for equality and inequality.

# Features:\n
# (*) Implements complex numbers with real and imaginary parts.\n
# (*) Supports arithmetic operations: addition, subtraction, multiplication, and division.\n
# (*) Provides methods for absolute value calculation and comparison.\n
# (*) Designed for simplicity and ease of use."""
# )
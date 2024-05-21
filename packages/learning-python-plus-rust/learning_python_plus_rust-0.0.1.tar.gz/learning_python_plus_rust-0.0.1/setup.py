from setuptools import setup, find_packages


# Defines the README.md as the long description of the package
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="learning_python_plus_rust",
    version="0.0.1",
    author="João Pedro Areias de Moraes",
    author_email="joaoareiasmoraes@gmail.com",
    description='My implementation of the book "Speed Up Your Python Program with Rust" by Adam Kleczkowski',
    long_description=long_description,
    url="https://github.com/JoaoAreias/learning-python-plus-rust",
    install_requires=[],
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    test_requires=["pytest"],
    entry_points={
        "console_scripts": [
            "fib-number = learning_python_plus_rust.cmd.fib_numb:fib_numb",
        ],
    },
)

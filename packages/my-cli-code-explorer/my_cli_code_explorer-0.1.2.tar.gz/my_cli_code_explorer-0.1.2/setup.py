# setup.py

from setuptools import setup, find_packages

setup(
    name="my_cli_code_explorer",  # Ensure your package name is consistent
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "typer[all]",  # Install Typer with its dependencies
    ],
    entry_points={
        "console_scripts": [
            "my_cli_code_explorer=my_cli_code_explorer.main:app",  # Correct the entry point
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)

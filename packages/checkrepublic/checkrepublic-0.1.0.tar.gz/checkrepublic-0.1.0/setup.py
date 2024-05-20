from setuptools import setup, find_packages

setup(
    name="checkrepublic",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Nick Schrock",
    description="A lightweight python library for runtime invariant checking.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/checkrepublic",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

from setuptools import setup, find_namespace_packages

description = "InterSystems IRIS component of testcontainers-python."

setup(
    packages=find_namespace_packages(),
    description=description,
    install_requires=[
        "testcontainers-core",
        "sqlalchemy",
        "sqlalchemy-iris",
        "requests<2.32.0"
    ],
    python_requires=">=3.7",
)

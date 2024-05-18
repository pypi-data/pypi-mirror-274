from setuptools import setup, find_packages

setup(
    name='empower_functions',  # This is the package name
    version='0.1',
    packages=find_packages(),  # This will find the `empower_functions` directory
    install_requires=[
        "jinja2",
        "llama-cpp-python[server]",
        "pydantic"
        # Add your dependencies here
    ],
)

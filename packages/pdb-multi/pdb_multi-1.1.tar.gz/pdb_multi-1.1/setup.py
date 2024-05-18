from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="pdb_multi",
    version="1.1",
    py_modules=["pdb_multi"],
    description="Pdb designed for multiprocessing",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/claserken/pdb-multi"
)
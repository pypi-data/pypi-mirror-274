from setuptools import setup, find_packages

setup(
    name='FuPy',
    version='0.0.1',
    packages=find_packages(),
    description='Functional Programming in Python, for Education',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tom Verhoef (Eindhoven University of Technology)',
    author_email='T.Verhoeff@tue.nl',
    url='https://gitlab.tue.nl/t-verhoeff-software/FuPy',
    license='MIT',
)

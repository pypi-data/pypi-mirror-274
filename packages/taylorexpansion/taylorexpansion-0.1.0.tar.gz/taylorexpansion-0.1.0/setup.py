# setup.py

from setuptools import setup, find_packages

setup(
    name='taylorexpansion',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'sympy',
    ],
    description='A package to compute the Taylor series expansion of a given function.',
    author='vikkivarma16',
    author_email='vikkivarma16@gmail.com',
    url='https://github.com/vikkivarma16/taylorexpansion',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)


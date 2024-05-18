# setup.py

from setuptools import setup, find_packages

setup(
    name="notebook2md",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'nbformat',
        'nbconvert'
    ],
    entry_points={
        'console_scripts': [
            'notebook2md=notebook2md.converter:convert_ipynb_to_md',
        ],
    },
    author="Shpetim Haxhiu",
    author_email="shpetim.h@gmail.com",
    description="A package to convert Jupyter notebooks to Markdown files",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shpetimhaxhiu/notebook2md",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

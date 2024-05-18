from os import path
from setuptools import setup, find_packages


def get_long_description():
  here = path.abspath(path.dirname(__file__))
  with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="meta-json",
    version="1.0.0",
    description="Extract metadata from a deserialized JSON.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/juangcr/meta_json",
    author="Juan Cortés",
    author_email="juang.cortes@outlook.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent"
    ],
    keywords='metadata json',
    include_package_data=True,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    extras_require={
        "test": [
            "coverage",
            "pytest",
            "black",
            "flake8",
            "mypy"
            ]
    },
)


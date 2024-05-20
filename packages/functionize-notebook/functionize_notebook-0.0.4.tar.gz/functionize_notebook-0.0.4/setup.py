from distutils.core import setup
from setuptools import find_packages

setup(
    name="functionize-notebook",
    version="0.0.4",
    author="Bui Hoang Tu",
    author_email="bhtu.work@gmail.com",
    url="https://github.com/BuiHoangTu/functionize-notebook/tree/release",
    license="MIT",
    packages=find_packages(),
    package_dir={"notebook_wrapper": "notebook_wrapper"},
    description="run notebook like a function",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=["nbformat", "nbconvert"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
)

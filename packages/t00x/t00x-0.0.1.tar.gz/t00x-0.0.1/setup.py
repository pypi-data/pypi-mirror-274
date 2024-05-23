from setuptools import setup, find_packages

setup(
    name="t00x",
    version="0.0.1",
    author="t00x t00x",
    author_email="t00x@t00x.com",
    description=".",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta"
    ],
    python_requires='>=3.6',
)
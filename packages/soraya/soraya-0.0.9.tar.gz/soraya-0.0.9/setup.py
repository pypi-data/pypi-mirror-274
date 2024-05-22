import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "soraya",
    version = "0.0.9",
    author = "Hassan Gashmard",
    author_email = "HassanGashmard@gmail.com",
    description = "Soraya is a package that selects the most important features using an innovative hybrid method for both regression and classification problems.",
    long_description = long_description,
    license="MIT",
    long_description_content_type = "text/markdown",
    url = "https://github.com/Gashmard/Soraya",

    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = setuptools.find_packages(),
    python_requires = ">=3.6"
)


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "jabir",
    version = "0.0.7",
    author = "Hassan Gashmard",
    author_email = "HassanGashmard@gmail.com",
    description = "jabir is a package that generates 322 features for any material.",
    long_description = long_description,
    license="MIT",
    long_description_content_type = "text/markdown",
    url = "https://github.com/Gashmard/jabir",

    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = setuptools.find_packages(),
    python_requires = ">=3.6"
)


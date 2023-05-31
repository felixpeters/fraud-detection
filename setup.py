import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fraud-detection",
    version="0.1.0",
    author="Felix Peters",
    description="Full-stack ML case study for credit card fraud detection.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felixpeters/fraud-detection",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

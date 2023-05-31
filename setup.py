import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ai-project-template",
    version="0.1.0",
    author="Felix Peters",
    description="Template for developing AI projects according to proven principles and best practices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felixpeters/ai-project-template",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

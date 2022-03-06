import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as f:
    version = f.read().strip()

with open("requirements.txt", "r") as f:
    install_requires = f.readlines()

setuptools.setup(
    name="scidownl",
    version=version,
    author="Tishacy",
    author_email="Tishacy@gmail.com",
    description="Download pdfs from Scihub.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tishacy/SciDownl",
    packages=setuptools.find_packages(exclude=["test.*", "test"]),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'scidownl=scidownl.api.cli:cli'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)

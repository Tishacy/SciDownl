import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scidownl",
    version="0.2.2",
    author="Tishacy",
    author_email="Tishacy@gmail.com",
    description="Download pdfs from Scihub via DOI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tishacy/SciDownl",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['termcolor>=1.1.0','mspider>=0.2.5',
                      'requests>=2.18.4','Pillow>=6.0.0', 'beautifulsoup4>=4.7.1'],
    entry_points={
        'console_scripts': [
            'scidownl=scidownl.scidownl:main'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

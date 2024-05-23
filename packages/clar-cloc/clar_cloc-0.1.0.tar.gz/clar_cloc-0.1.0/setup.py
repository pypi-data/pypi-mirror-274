from setuptools import setup, find_packages

setup(
    name="clar-cloc",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "tabulate",
        "setuptools"
    ],
    entry_points={
        "console_scripts": [
            "clar-cloc=clar_cloc.cli:main",
        ],
    },
    author="Kristian Apostolov",
    author_email="kristianapostolovcontacts@gmail.com",
    description="A CLI tool to count lines in Clarity (.clar) files",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/clar_cloc",
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)

# Clarity Line Counter

A CLI tool to count lines in Clarity (.clar) files.

## Installation

You can install the tool using `pip`:

```bash
pip3.12 install git+https://github.com/CrisCodesCrap/clar_cloc.git
```

## Usage

To use the tool, navigate to the directory containing the .clar files and run:

```bash
clar-cloc --exclude-dirs "exclude_this,and_this"
```

- `--exclude-dirs` (optional): Comma-separated list of directories to exclude.

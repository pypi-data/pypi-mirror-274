import click

from os import getcwd
from os.path import abspath, join

from typing import List

from clar_cloc.count import process_directory


@click.command()
@click.option('--exclude-dirs', default="", help='Comma-separated list of directories to exclude.')
def main(exclude_dirs: str) -> None:
    cwd: str = getcwd()
    exclude: List[str] = [abspath(join(cwd, d.strip())) for d in exclude_dirs.split(',')]
    process_directory(cwd, exclude)

if __name__ == "__main__":
    main()

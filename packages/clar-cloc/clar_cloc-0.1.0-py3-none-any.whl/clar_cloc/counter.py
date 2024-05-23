from os import getcwd, walk
from os.path import abspath, join, relpath

from typing import List, Tuple, Optional

from tabulate import tabulate

# Types:
Total = Tuple[int, int, int] # source, blank, comment
Totals = Tuple[int, int, int, int]  # source, blank, comment, count
Results = List[List] # relative path, source, blank, comment

# Constants:
#  -> Clarity:
BLANK: str = ""
COMMENT: str = ";;"
FILE_EXTENSION: str = ".clar"

#  -> Output:
TABLE_HEADERS: List[str] = ["File", "Source lines", "Blank lines", "Comment lines"]
TABLE_FORMAT: str = "rounded_grid"

# -> Errors:
ERROR_DIRECTORY_NOT_FOUND: str = "Directory not found"
ERROR_FILE_NOT_FOUND: str = "File not found"
ERROR_READING_DIRECTORY: str = "An error occurred while reading directory"
ERROR_READING_FILE: str = "An error occurred while reading file"
ERROR_NO_FILES_FOUND: str = f"No {FILE_EXTENSION} files found"


def error(message: str, var: Optional[str] = None) -> None:
    raise Exception(f"ERROR: {message}{f': {var}' if var else ''}.")

def _count_lines(path: str) -> Total:
    source, blank, comment = 0, 0, 0
    with open(path, 'r') as file:
        for line in file:
            stripped: str = line.strip()
            
            if stripped == BLANK: blank += 1
            elif stripped.startswith(COMMENT): comment += 1
            else: source += 1

    return source, blank, comment

def count_lines(path: str) -> Total:
    try:
        return _count_lines(path)
    
    except FileNotFoundError: error(ERROR_FILE_NOT_FOUND, path)
    except IOError: error(ERROR_READING_FILE, path)

def log(results: Results, totals: Totals) -> None:
    if not results: error(ERROR_NO_FILES_FOUND)
        
    print(tabulate(results, headers=TABLE_HEADERS, tablefmt=TABLE_FORMAT))

    totals_row = [["Total", totals[0], totals[1], totals[2]]]
    print(tabulate(totals_row, headers=TABLE_HEADERS, tablefmt=TABLE_FORMAT))
    print(f"Total files processed: {totals[3]}")
    

def process_directory(path: str, exclude: List[str]) -> None:
    totals: Totals = (0, 0, 0, 0)
    results: Results = []

    try:
        for root, dirs, files in walk(path):
            # Skip directories that are in the exclude list
            dirs[:] = [d for d in dirs if join(root, d) not in exclude]

            for file in files:
                if not file.endswith(FILE_EXTENSION): continue

                abs_path = join(root, file)
                relative = relpath(abs_path, path)
                counts = count_lines(abs_path)
                
                totals = (
                    totals[0] + counts[0],
                    totals[1] + counts[1],
                    totals[2] + counts[2],
                    totals[3] + 1
                )
                
                results.append([relative, *counts])

        log(results, totals)
    except FileNotFoundError: error(ERROR_DIRECTORY_NOT_FOUND, path)
    except IOError:
        error(ERROR_READING_DIRECTORY, path)

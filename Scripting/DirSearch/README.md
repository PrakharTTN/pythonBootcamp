
# DirSearcher

A Python command-line utility to search for files and directories within a specified directory — built without using external libraries for searching.

This tool supports flexible options for filtering files based on name, type, access time, and recursion depth.

## Features

- **Search by Name**: Use wildcards like `*.txt` or `myfile*` to search for files matching a specific pattern.
- **Filter by Type**: Search for files (`-type f`) or directories (`-type d`).
- **Access Time Filter**: Find files accessed within the last `N` days (`-atime N`).
- **Depth Control**: Limit the depth of recursion to avoid deep, unnecessary searches with `-maxdepth N`.
- **Recursively Search Subdirectories**: Supports recursive searching up to a specified depth.
- **Cross-platform**: Works across all major operating systems, as long as Python is installed.

## Usage

```bash
python dir_searcher.py DIRECTORY [OPTIONS]
```

### Required Argument

- `DIRECTORY`: The directory in which to begin the search. If not provided, the current directory is used.

### Optional Arguments

| Option          | Description                                                                       |
| --------------- | --------------------------------------------------------------------------------- |
| `-name NAME`    | Filter by filename pattern (supports wildcards like `*.txt`).                    |
| `-type TYPE`    | Filter by file type (`f` for files, `d` for directories).                        |
| `-atime N`      | Search for files accessed within the last `N` days.                              |
| `-maxdepth N`   | Limit the recursion depth to `N` levels of subdirectories.                       |

> Note: In case multiple filters are applied, the search results are narrowed down based on all provided criteria.

## Example

#### Find all `.py` files in the current directory and its immediate subdirectories:

```bash
python dir_searcher.py . -name "*.py" -maxdepth 1
```

#### Find all files (not directories) that were accessed within the last 7 days:

```bash
python dir_searcher.py . -type f -atime -7
```

#### Search for all directories that match a specific pattern and are within 2 levels of subdirectories:

```bash
python dir_searcher.py /path/to/search -name "mydir*" -type d -maxdepth 2
```

#### Find all `.txt` files in the home directory and all subdirectories with a depth limit of 3:

```bash
python dir_searcher.py ~/ -name "*.txt" -maxdepth 3
```

## Implementation Notes

- The script does **not rely on third-party libraries** like `os` and `time` for file search and manipulation.
- The search is done recursively, with optional depth control (`-maxdepth`) to limit subdirectory traversal.
- The access time filter uses the system's last access time, and the script performs basic error handling for file access.

## Limitations

- Assumes that file paths and names do not contain complex special characters or require escape sequences.
- Does not handle symbolic links or other special file types that might require additional handling.
- Performance can degrade on directories with a large number of files, especially when recursion depth is high.


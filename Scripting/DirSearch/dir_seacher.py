import os
import time
import argparse
import fnmatch
from typing import Optional, List


def find_files(
    directory: Optional[str] = None,
    name: Optional[str] = None,
    file_type: Optional[str] = None,
    atime: Optional[str] = None,
    maxdepth: Optional[str] = None,
) -> List[str]:
    """
    Search for files or directories in the specified directory that match the provided criteria.

    Args:
        directory (Optional[str]): The directory to start the search. Defaults to the current working directory.
        name (Optional[str]): A pattern to match filenames (e.g., '*.txt'). Defaults to None (no filename filter).
        file_type (Optional[str]): The type of file to search for ('f' for files, 'd' for directories). Defaults to None (search both).
        atime (Optional[int]): The number of days since the file was last accessed. Files accessed in the last `atime` days will be returned. Defaults to None (no access time filter).
        maxdepth (Optional[int]): The maximum depth of recursion for subdirectories. Defaults to None (no depth limit).

    Returns:
        List[str]: A list of file or directory paths that match the search criteria.

    Example:
        find_files("/path/to/dir", name="*.py", file_type="f", atime=7, maxdepth=2)
        This will search for Python files in the specified directory and its subdirectories,
        which were accessed in the last 7 days, up to a depth of 2.
    """
    results = []  # Final result list. It'll have all the desired outputs
    current_time = time.time()

    # If directory is None or not provided, take the current dir as directory
    if directory is None:
        directory = os.getcwd()

    # Make sure directory is absolute and time is in seconds
    directory = os.path.abspath(directory)
    if atime is not None:
        atime = atime * 86400  # Convert days to seconds

    def dir_search(directory, atime, file_type, depth=0):
        if (
            maxdepth is not None and depth >= maxdepth
        ):  # Break condition when maxdepth reached
            return
        try:
            # Loop through directory contents
            for i in os.listdir(directory):
                full_path = os.path.join(directory, i)

                if file_type == "f" or file_type is None:
                    # Search for files
                    if os.path.isfile(full_path) and (
                        name is None
                        or fnmatch.fnmatch(i, name)
                        and (
                            atime is None
                            or atime > (current_time - os.path.getatime(full_path))
                        )
                    ):
                        results.append(full_path)

                elif file_type == "d":
                    # Search for directories
                    if os.path.isdir(full_path) and (
                        name is None
                        or fnmatch.fnmatch(i, name)
                        and (
                            atime is None
                            or atime > (current_time - os.path.getatime(full_path))
                        )
                    ):
                        results.append(full_path)

                # Recursively search subdirectories
                if os.path.isdir(full_path):
                    dir_search(full_path, atime, file_type, depth + 1)

        except PermissionError:
            pass  # Ignore directories that require sudo permissions

    dir_search(directory, atime, file_type, depth=0)
    return results


if __name__ == "__main__":
    # Create a parser to parse the command-line arguments
    parser = argparse.ArgumentParser(
        description="Find files in a directory with various filters."
    )

    # Arguments for the parser
    parser.add_argument(
        "directory",
        nargs="?",
        default=os.getcwd(),
        help="The directory which you want as the starting point (default = current working directory)",
    )
    parser.add_argument(
        "-name", type=str, help="Filter by filename (supports patterns like '*.txt')."
    )
    parser.add_argument(
        "-type",
        choices=["f", "d"],
        help="Filter by type: 'f' for files, 'd' for directories.",
    )
    parser.add_argument(
        "-atime", type=int, help="Find files accessed within the last N days."
    )
    parser.add_argument(
        "-maxdepth", type=int, help="Maximum depth for recursive search."
    )

    # Parse the args and return the results from the function in a list variable
    args = parser.parse_args()
    results = find_files(
        args.directory, args.name, args.type, args.atime, args.maxdepth
    )

    # Print the results
    if results:
        for i in results:
            print(i)
    else:
        print("No results found.")

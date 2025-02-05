import os
import argparse
import fnmatch
import time
def find_files(directory, name=None, file_type=None, atime=None, maxdepth=None):
    """
    Search for files in the given directory based on name, type, access time, and max depth.
    """
    results = []
    current_time = time.time()
    directory = os.path.abspath(directory)

    def search_dir(path, depth):
        if maxdepth is not None and depth > maxdepth:
            return

        try:
            for entry in os.scandir(path):
                # Ensure correct file type filtering
                if file_type == 'f' and not entry.is_file():
                    continue
                if file_type == 'd' and not entry.is_dir():
                    continue

                # Match filename pattern
                if name and not fnmatch.fnmatch(entry.name, name):
                    continue
                results.append(entry.path)

                if entry.is_dir():
                    search_dir(entry.path,depth+1)    
                              # Match access time
                if atime is not None:
                    last_access_days = (current_time - os.stat(entry.path).st_atime) / 86400
                    if atime < 0 and last_access_days > abs(atime):  # accessed within last X days
                        continue
                    elif atime > 0 and last_access_days < atime:  # accessed before X days
                        continue

                results.append(entry.path)

                # Recursively search subdirectories
                if entry.is_dir():
                    search_dir(entry.path, depth + 1)

        except PermissionError:
            pass  # Ignore directories that require elevated permissions

    search_dir(directory, 0)
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find files based on name, type, access time, and depth.")
    parser.add_argument("directory", help="Directory to search in")
    parser.add_argument("-name", help="Filename pattern (supports wildcards like '*.py')")
    parser.add_argument("-type", choices=['f', 'd'], help="Type: 'f' for files, 'd' for directories")
    parser.add_argument("-atime", type=int, help="Access time: -X for files accessed in last X days, X for older")
    parser.add_argument("-maxdepth", type=int, help="Maximum depth to search")

    args = parser.parse_args()
    results = find_files(args.directory, args.name, args.type, args.atime, args.maxdepth)

    if results:
        print("\n".join(results))
    else:
        print("No matching files found.")

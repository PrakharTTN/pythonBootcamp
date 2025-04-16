import argparse
from typing import List, Optional


def guess_delimiter(content: str) -> str:
    """
    Guess the delimiter used in a CSV content string.

    Args:
        content: The full text content of the CSV file.

    Returns:
        The most frequent delimiter found: ',', ';', or tab.
    """
    delimiter_dict = {
        ',': content.count(','),
        '\t': content.count('\t'),
        ';': content.count(';')
    }

    return max(delimiter_dict, key=delimiter_dict.get)


def parsecsv(
    file: str,
    delimiter: Optional[str] = None,
    skiprows: int = 0,
    headrows: Optional[int] = None,
    tailrows: Optional[int] = None,
    columns: Optional[str] = None
) -> List[List[str]]:
    """
    Parses the CSV file and extracts data based on the provided options.

    Args:
        file: Path to the CSV file.
        delimiter: Optional delimiter to use. Guessed if not provided.
        skiprows: Number of initial rows to skip.
        headrows: Show only the first N data rows.
        tailrows: Show only the last N data rows.
        columns: Comma-separated 1-based column indices to display.

    Returns:
        List of rows (each row is a list of strings).
    """
    with open(file, 'r') as f:
        lines = f.readlines()

    header = lines[0].strip()
    datalines = lines[1:]

    if delimiter is None:
        delimiter = guess_delimiter(''.join(lines))

    data = [header.split(delimiter)]

    if skiprows:
        datalines = datalines[skiprows:]

    for line in datalines:
        line = line.strip()
        if not line:
            continue
        row = line.split(delimiter)
        data.append(row)

    # Filter specific columns (1-based index)
    if columns:
        column_indices = [int(c) - 1 for c in columns.split(',')]
        data = [[row[i] for i in column_indices if i < len(row)] for row in data]

    if headrows is not None:
        data = data[:headrows]
    elif tailrows is not None:
        data = data[-tailrows:]

    return data


def print_table(data: List[List[str]]) -> None:
    """
    Prints the CSV data in a nicely formatted table.

    Args:
        data: The parsed CSV data as a list of rows.
    """
    if not data:
        print("No data to display.")
        return

    num_columns = len(data[0])
    column_widths = [0] * num_columns

    for row in data:
        for i, item in enumerate(row):
            column_widths[i] = max(column_widths[i], len(str(item)))

    for row in data:
        print("  ".join(str(item).ljust(column_widths[i]) for i, item in enumerate(row)))


def main() -> None:
    """
    Entry point for the CLI utility. Parses arguments and processes the CSV file.
    """
    parser = argparse.ArgumentParser(description="Display CSV content in a table.")
    parser.add_argument('file', help="CSV file to process.")
    parser.add_argument('-d', '--delimiter', help="CSV delimiter (default: auto-detect).")
    parser.add_argument('--skip-row', type=int, default=0, help="Skip the first N rows (excluding header).")
    parser.add_argument('--head', type=int, help="Display only the first N data rows.")
    parser.add_argument('--tail', type=int, help="Display only the last N data rows.")
    parser.add_argument('-f', '--columns', help="Comma-separated column numbers to show (1-based index).")

    args = parser.parse_args()

    data = parsecsv(
        file=args.file,
        delimiter=args.delimiter,
        skiprows=args.skip_row,
        headrows=args.head,
        tailrows=args.tail,
        columns=args.columns
    )

    print_table(data)


if __name__ == '__main__':
    main()

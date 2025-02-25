import argparse

def guess_delimiter(content):
    delimiter_dict = {
        ',':0,
        '\t':0,
        ';':0
    }
    delimiter_dict[',']=content.count(',')
    delimiter_dict[';']=content.count(';')
    delimiter_dict['\t']=content.count('\t')
    
    return max(delimiter_dict, key=delimiter_dict.get)

def parsecsv(file, delimiter=None, skiprows=0, headrows=None, tailrows=None, columns=None):
    with open(file, 'r') as file:
        lines = file.readlines()

    #added the first line as title
    header = lines[0].strip()
    datalines = lines[1:]
    data = []

    #guess the delimiter if none provided
    if delimiter is None:
        delimiter = guess_delimiter(''.join(lines))
        data = [header.split(delimiter)]

    #skip the first N rows if needed
    if skiprows:
        datalines = datalines[skiprows:]

    for line in datalines:
        line = line.strip()
        if not line:
            continue

        # Split the line by the delimiter
        row = line.split(delimiter)

        # Add the row to the data
        data.append(row)

    #filter the data to only those columns
    if columns:
        columns = [int(c) - 1 for c in columns.split(',')]  # Convert to 0-based indexing
        for row in data:
            for i in columns:
                if i<len(row):
                    data=row[i]
        data = [[row[i] for i in columns if i < len(row)] for row in data]

    if headrows:
        data = data[:headrows]
    elif tailrows:
        data = data[-tailrows:]

    return data

def print_table(data):
    if not data:
        print("No data to display.")
        return

    # Determine column widths without using zip(*data)
    num_columns = len(data[0])
    column_widths = [0] * num_columns

    for row in data:
        for i, item in enumerate(row):
            column_widths[i] = max(column_widths[i], len(str(item)))

    # Print each row
    for row in data:
        print("  ".join(str(item).ljust(column_widths[i]) for i, item in enumerate(row)))


def main():
    parser = argparse.ArgumentParser(description="Process a CSV file.")
    
    # Define the arguments
    parser.add_argument('file', help="CSV file to process.")
    parser.add_argument('-d', '--delimiter', help="Delimiter for the CSV file.")
    parser.add_argument('--skip-row', type=int, default=0, help="Number of rows to skip at the beginning.")
    parser.add_argument('--head', type=int, help="Number of rows to display from the start.")
    parser.add_argument('--tail', type=int, help="Number of rows to display from the end.")
    parser.add_argument('-f', '--columns', help="Columns to shpw.")

    # Parse the arguments
    args = parser.parse_args()
    data = parsecsv(args.file, args.delimiter, args.skiprows, args.headrows, args.tailrows, args.columns)
    print_table(data)

if __name__ == '__main__':
    main()

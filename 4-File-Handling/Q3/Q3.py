import sys

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

def parse_csv(file, delimiter=None, skip_rows=0, head_rows=None, tail_rows=None, columns=None):
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
    if skip_rows:
        datalines = datalines[skip_rows:]

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
        data = [[row[i] for i in columns if i < len(row)] for row in data]

    #only return the first N rows
    if head_rows:
        data = data[:head_rows]

    #only return the last N rows
    if tail_rows:
        data = data[-tail_rows:]

    return data

def print_table(data):
    if not data:
        print("No data to display.")
        return

    #calculate the max width of each column for pretty printing
    column_widths = [max(len(str(item)) for item in column) for column in zip(*data)]

    #print each row
    for row in data:
        row_string = "  ".join(str(item).ljust(column_widths[i]) for i, item in enumerate(row))
        print(row_string)

def main():
    delimiter = None
    skip_rows = 0
    head_rows = None
    tail_rows = None
    columns = None
    file = "email.csv"

    args = sys.argv[1:]

    # Parse the command-line arguments
    while args:
        arg = args.pop(0)
        if arg == '-d':
            delimiter = args.pop(0)
        elif arg == '--skip-row':
            skip_rows = int(args.pop(0))
        elif arg == '--head':
            head_rows = int(args.pop(0))
        elif arg == '--tail':
            tail_rows = int(args.pop(0))
        elif arg == '-f':
            columns = args.pop(0)
        else:
            file = arg

    if not file:
        print("Error: Please provide a CSV file.")
        return

    data = parse_csv(file, delimiter, skip_rows, head_rows, tail_rows, columns)
    print_table(data)

if __name__ == '__main__':
    main()

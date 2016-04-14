#!/usr/bin/env python3

"""
MediaWiki Table Converter
Converts a table from comma-separated values (csv) to 
MediaWiki-compatible markup. Prints the results to stdout.
"""
import argparse
import re

parser = argparse.ArgumentParser(description="Converts a table from comma-separated values " +
    "(csv) to MediaWiki-compatible markup. Prints result to stdout.")
parser.add_argument("file", help="CSV file to convert")
parser.add_argument("-c", "--caption", help="Optional table caption/title", action="store",
    type=str, default="")
parser.add_argument("-H", "--header", 
    help="Treat first line as column labels (make text bold). Same as -b 1",
    action="store_true")
parser.add_argument("-b", "--bold-rows", 
    help="Make the first N rows bold. If N=1, this is the same as -H.", action="store", 
    type=int, default=0)

# Stuff to escape non-layout commas (i.e. commas that are part of cell contents)
# Assumes cells containing commas are enclosed in quotes
escaped_comma_exp = '(".*?,.*?")' # Regular expression for an escaped comma
escape_sequence = '^&^&^&' # Replaces escaped commas
def escape_comma(matchobj):
    """Escapes non-layout commas inside cells. Accepts a re.match object and
    returns a string with the comma substituted by escape_sequence and
    the leading and trailing quotes (csv escape characters) removed. To be used
    with the re.sub method.
    """
    # Substitute the comma
    repl = matchobj.group(0).replace(',', escape_sequence)
    # Remove the outer quotes
    repl = repl[1:-1]
    return repl


def dump_wikitable(csv_string, caption=None, bold_to_row=0):
    """Returns a string with MediaWiki-compatible table markup.
    Keyword args:
        csv_string -- Table as a string of comma-separated values (str)
        caption -- Optional caption (title) for table (str)
        bold_to_row -- Optional number of rows from the top to mark as header (int)
    """
    # Substitute any commas that are escaped with quotes
    csv_string = re.sub(escaped_comma_exp, escape_comma, csv_string)
    csvtable = csv_string.split('\n')
    rows = ['{| class="wikitable"', ]
    for n in range(len(csvtable)):
        if n == 0 and caption:
            rows.append("|+%s" %caption)
        if n in range(bold_to_row):
            rows.append("!%s\n|-" %'!!'.join(csvtable[n].split(',')))
        else:
            rows.append("|%s\n|-" %'||'.join(csvtable[n].split(',')))
    # Replace any non-layout commas that were substituted
    rows = [row.replace(escape_sequence, ',') for row in rows]
    return '\n'.join(rows) + '\n|}'


if __name__ == "__main__":
    args = parser.parse_args()
    if args.header:
        bold_rows = 1
    elif args.bold_rows > 0:
        bold_rows = args.bold_rows
    else:
        bold_rows = 0
    with open(args.file, 'r') as f:
        csv_str = f.read()
    wikitable = dump_wikitable(csv_str, args.caption, bold_rows)
    print(wikitable)

#!/usr/bin/env python3

"""
MediaWiki Table Converter
Converts a table from comma-separated values (csv) to 
MediaWiki-compatible markup. Prints the results to stdout.
"""
import argparse

parser = argparse.ArgumentParser(description="Converts a table from comma-separated values " +
    "(csv) to MediaWiki-compatible markup. Prints result to stdout.")
parser.add_argument("file", help="CSV file to convert")
parser.add_argument("-H", "--header", help="Treat first line as column labels (make text bold).",
    action="store_true")

def dump_wikitable(csv_string):
    csvtable = csv_string.split('\n')
    newtable = '{| class="wikitable"\n'
    firstrow = True
    for row in csvtable:
        for cell in row.split(','): #XXX How does csv escape commas in cells?
            if firstrow:
                newtable = newtable + "!%s\n" %cell
            else:
                newtable = newtable + "|%s\n" %cell
        newtable = newtable + "|-\n"
        firstrow = False
    newtable = newtable + "|}"
    return newtable


if __name__ == "__main__":
    args = parser.parse_args()
    with open(args.file, 'r') as f:
        csv_str = f.read()
    wikitable = dump_wikitable(csv_str)
    print(wikitable)

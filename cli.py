from argparse import ArgumentParser
import csv
import os.path
import sys

from visa_desjardins_statement_parser import extract_transactions

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


parser = ArgumentParser(description="Visa Desjardins Statement Parser")
parser.add_argument("-i", dest="filename", required=True,
                    help="Relevé Visa Desjardins", metavar="FILE",
                    type=lambda x: is_valid_file(parser, x))
args = parser.parse_args()

filename = args.filename

transactions = extract_transactions(filename)

fieldnames=transactions[0].keys()
csv_writer = csv.DictWriter(sys.stdout, delimiter=';', quotechar='"', lineterminator='\n', fieldnames=fieldnames)
csv_writer.writeheader()
data_to_write = transactions
csv_writer.writerows(data_to_write)
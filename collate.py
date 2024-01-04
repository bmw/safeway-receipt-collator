#!/usr/bin/env python3
import argparse
import collections
import operator

parser = argparse.ArgumentParser(description='Combines totals from digital '
                                             'Safeway receipts')
parser.add_argument('receipts_file')

with open(parser.parse_args().receipts_file) as f:
    receipt_lines = f.read().splitlines()

current_item = None
purchases = collections.defaultdict(float)
for i, line in enumerate(receipt_lines):
    if line == 'Regular Price':
        assert current_item is None, 'Unexpected price while still parsing ' + current_item
        current_item = receipt_lines[i - 1]
    elif current_item and '$' in line and '/' not in line:
        purchases[current_item] += float(line[1:])
        current_item = None

total = 0
for item, price in sorted(purchases.items(), key=operator.itemgetter(1), reverse=True):
    total += price
    print(item, price)
print('TOTAL SPENT', total)

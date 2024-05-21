#!/usr/bin/env python3

import sys
import csv
from mdtables import Table, Column


def main():
	lines = list(csv.reader(sys.stdin, delimiter="\t"))

	if lines[0][0][0] == "#":
		t = Table(
			*(
				Column(field) \
					if i > 0 else field[1:] # Strip leading #
				for i, field in enumerate(lines[0])
			)
		)
		lines = lines[1:]
	else:
		t = Table(
			*(
				Column("") for field in lines[0]
			)
		)

	for line in lines:
		t.row(*line)

	print(t)

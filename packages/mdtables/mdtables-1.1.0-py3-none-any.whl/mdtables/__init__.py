#!/usr/bin/env python3

"""
mdtables — Python library to create Markdown tables
Copyright (C) 2017, Midgard

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <https://www.gnu.org/licenses/>.
"""

_ALCHARS = {"left": "<", "right": ">", "center": "^"}

class Column:
	def __init__(self, header, alignment="left", width=None, headerformat=None, fmt=None):
		self.header       = header
		self.alignment    = alignment
		self.width        = width

		self.dataformat   = fmt
		self.headerformat = headerformat


	def _formatstrpart(self, header):
		fmt = self.headerformat if header else self.dataformat
		return fmt if fmt is not None else ""


	def fitting_width_for(self, data, header=False):
		return len(
			("{:" + self._formatstrpart(header) + "}").format(data)
		)


	def format(self, data, width, header=False):
		return (
			"{:" + _ALCHARS.get(self.alignment, "") + str(width) + self._formatstrpart(header) + "}"
		).format(data)


	def create_line(self, width):
		return (
			(":" if self.alignment == "center" else "-") +
			"-"*(width-2) +
			(":" if self.alignment == "right" or self.alignment == "center" else "-")
		)


class Table:
	def __init__(self, *args, data=None):
		self.data     = list(map(tuple, data)) if data else []
		self.columns  = tuple(args)
		self.num_cols = len(self.columns)

		assert all(isinstance(c, Column) for c in self.columns)


	def row(self, *args):
		row = tuple(args)

		if len(row) != self.num_cols:
			raise ValueError("Row had {} columns, expected {}".format(len(row), self.num_cols))

		self.data.append(row)

		return self


	def __str__(self):
		col_widths = tuple(
			(
				column.width
				if column.width else
				max(
					3 if column.alignment == "center" else 2,
					column.fitting_width_for(column.header, True),
					*(column.fitting_width_for(row[col_index]) for row in self.data)
				)
			)
			for col_index, column in enumerate(self.columns)
		)

		return "\n".join(
			"|" + line + "|" for line in (
				"|".join(
					column.format(column.header, col_width, True)
					for column, col_width in zip(self.columns, col_widths)
				),
				"|".join(
					column.create_line(col_width)
					for column, col_width in zip(self.columns, col_widths)
				),
				*(
					"|".join(
						column.format(cell_data, col_width)
						for column, col_width, cell_data in zip(self.columns, col_widths, row)
					)
					for row in self.data
				)
			)
		)

import csv
import itertools
import json

from collections import defaultdict


def convert(filename):
  with open(filename, 'r') as f:
    d = json.load(f)
    for sheet in d["sheets"]:
      sheet2csv(sheet)


def sheet2csv(sheet):
  # Extract the data into a dict
  lastRow = 0
  lastCol = 0
  cells = defaultdict(lambda: defaultdict(str))
  for addr, cell in sheet["cells"].items():
    if "v" not in cell: continue
    val = cell['v']
    (row, col) = addr2rowcol(addr)
    lastRow = max(row, lastRow)
    lastCol = max(col, lastCol)
    cells[row][col] = val

  # Create a csv from the dict
  filename = f"out/{sheet['name']}.csv"
  with open(filename, 'w') as f:
    writer = csv.writer(f)

    for r in range(lastRow+1):
      row = [cells[r][c] for c in range(lastCol+1)]
      writer.writerow(row)

  print(f"wrote {filename}")


def addr2rowcol(addr):
  letters = itertools.takewhile(str.isalpha, addr)
  col = 0
  it = 0
  for c in letters:
    col += ord(c) - ord('A') + it * (ord('Z')-ord('A')+1)
    it += 1
  row = int(addr[it:]) - 1 # to make it 0-indexed
  return (row, col)


convert("data/raw.json")

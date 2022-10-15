#!/usr/bin/env python3

import PyPDF2
import sys
import os.path
import argparse


#@cli.command(name='rotate', help='args: .pdf file, pdf_page, num_rotations_CW_90deg')
#@click.argument('pdf_file', nargs=1, type=click.Path())
#@click.argument('page', default=1, nargs=1)
#@click.argument('num_rotations', default=1, nargs=1)
def pdf_rotateCW_90(pdf_file, pages_str_list, num_rotations_str_list=1):
  """
  Rotate a page 90deg clockwise in a .pdf file and save it to a new file
  Rotate multiple pages by making a list, eg python pdf.py -r test.pdf [1,2,3] [2,2,1]
  """
  # Process user input
  disallowed_chars = '[]'
  for ch in disallowed_chars:
    pages_str_list = pages_str_list.replace(ch, "")
    num_rotations_str_list = num_rotations_str_list.replace(ch, "")
  pages_str_list = pages_str_list.split(",")
  num_rotations_str_list = num_rotations_str_list.split(",")

  pages = []
  num_rotations = []

  try:
    assert pdf_file.split(".")[1] == 'pdf'
    assert os.path.isfile(pdf_file)
    assert len(pages_str_list) >= len(num_rotations_str_list)
    for i in pages_str_list:
      pages.append(int(i) - 1)
    for i in num_rotations_str_list:
      num_rotations.append(int(i))
    while len(pages) > len(num_rotations):
      num_rotations.append(1)
  except AssertionError:
    print('Use <filename.pdf> [pages] [num_rotations] as arguments')
    sys.exit()
  except:
    print('Page number and number of rotations must be integers')
    sys.exit()

  file = open(pdf_file, 'rb')
  reader = PyPDF2.PdfReader(file)
  writer = PyPDF2.PdfWriter()

  for page_num in range(len(reader.pages)):
    current_page = reader.pages[page_num]
    if page_num in pages:
      ind = pages.index(page_num)
      num_rotate = num_rotations[ind]
      for i in range(num_rotate):
        current_page.rotateClockwise(90)
    writer.add_page(current_page)

  filename = pdf_file.split(".")[0] + "_rotated.pdf"
  new_file = open(f'{filename}', 'wb')
  writer.write(new_file)
  print(f'New file {filename} created')

  file.close()
  new_file.close()


def pdf_concatenate(pdf_list):
  """
  Concatenates list of input .pdf files into a new concatenated .pdf file
  """
  try:
    assert len(pdf_list) > 1
    for file in pdf_list:
      assert file.split(".")[1] == 'pdf'
      assert os.path.isfile(file)
  except AssertionError:
    print('Use 2+ <filename.pdf> files as arguments')
    sys.exit()

  merger = PyPDF2.PdfMerger()
  for file in pdf_list:
    merger.append(file)

  filename = 'concatenated.pdf'
  merger.write(filename)
  print(f'New file {filename} created')

  merger.close()


#@cli.command(name='merge', help='args: 2+ tuples of (position to insert, .pdf file, pages (start, stop[, step]))')
#@click.argument('pdf_tuples', nargs=-1)
def pdf_merge(pdf_tuples):
  """
  Merge list of tuples (position to insert, .pdf file, pages (start, stop[, step])) into a new merged .pdf file
  """
  try:
    print('1')
    assert len(pdf_tuples) > 1
    print('2')
    for tuple in pdf_tuples:
      print('3')
      assert len(tuple) == 3
      print('4')
      assert tuple[1].split(".")[1] == 'pdf'
      print('5')
      assert os.path.isfile(tuple[1])
      print('6')
  except:
    print('Use tuples: (position to insert [0:], <filename.pdf>, (start, stop[, step])) as arguments')
    sys.exit()

  merger = PyPDF2.PdfMerger()
  for tuple in pdf_tuples:
    merger.merge(position=tuple[0], fileobj=tuple[1], pages=tuple[2])

  filename = 'merged.pdf'
  merger.write(filename)
  print(f'New file {filename} created')

  merger.close()


def pdf_delete(pdf_file, pages_str):
  """
  Delete pages from a .pdf file and save it to a new file
  """
  pages = []

  try:
    assert pdf_file.split(".")[1] == 'pdf'
    assert os.path.isfile(pdf_file)
    for i in pages_str:
      pages.append(int(i) - 1)
  except AssertionError:
    print('Use <filename.pdf> as an argument')
    sys.exit()
  except:
    print('Pages to be deleted must be integers')
    sys.exit()

  file = open(pdf_file, 'rb')
  reader = PyPDF2.PdfReader(file)
  writer = PyPDF2.PdfWriter()

  for page_num in range(len(reader.pages)):
    if not page_num in pages:
      current_page = reader.pages[page_num]
      writer.add_page(current_page)

  filename = pdf_file.split(".")[0] + "_deleted.pdf"
  new_file = open(f'{filename}', 'wb')
  writer.write(new_file)
  print(f'New file {filename} created')

  file.close()
  new_file.close()


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Manipulate .pdf files")
  group = parser.add_mutually_exclusive_group()
  group.add_argument('-c', '--concatenate', nargs='+', metavar='FILENAME.PDF')
  group.add_argument('-d', '--delete', nargs='+', metavar=('FILENAME.PDF', 'PAGE'))
  group.add_argument('-m', '--merge', nargs=4, action='append', metavar=('PG_INSERT', 'FILENAME.PDF', 'PG_START', 'PG_END'))
  group.add_argument('-r', '--rotate', nargs=3, metavar=('FILENAME.PDF', '[PAGES]', '[NUM_ROTATIONS_CW_90DEG]'))

  args = parser.parse_args()

  if args.concatenate:
    pdf_concatenate(args.concatenate)
  elif args.delete:
    pdf_delete(args.delete[0], args.delete[1:])
  elif args.merge:
    print(f'3 {args.merge}')            # 3 [['0', 'wtr.pdf', '0', '0'], ['1', 'twopage.pdf', '0', '1']]
  elif args.rotate:
    pdf_rotateCW_90(args.rotate[0], args.rotate[1], args.rotate[2])
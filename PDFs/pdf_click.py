#!/usr/bin/env python3

import PyPDF2
import sys
import os.path
import click


@click.group()
def cli():
  pass


@cli.command(name='rotate', help='args: .pdf file, pdf_page, num_rotations_CW_90deg')
@click.argument('pdf_file', nargs=1, type=click.Path())
@click.argument('page', default=1, nargs=1)
@click.argument('num_rotations', default=1, nargs=1)
def pdf_rotateCW_90(pdf_file, page=1, num_rotations=1):
  """
  Rotate a page 90deg clockwise in a .pdf file and save it to a new file
  """
  try:
    assert pdf_file.split(".")[1] == 'pdf'
    assert os.path.isfile(pdf_file)
  except:
    print('Please use <filename.pdf> as an argument')
    sys.exit()

  file = open(pdf_file, 'rb')
  reader = PyPDF2.PdfReader(file)
  writer = PyPDF2.PdfWriter()

  for page_num in range(len(reader.pages)):
    current_page = reader.pages[page_num]
    if page_num == (page - 1):
      for i in range(num_rotations):
        current_page.rotateClockwise(90)
    writer.add_page(current_page)

  filename = pdf_file.split(".")[0] + "_rotated.pdf"
  new_file = open(f'{filename}', 'wb')
  writer.write(new_file)
  print(f'New file {filename} created')

  file.close()
  new_file.close()


@cli.command(name='concatenate', help='args: concatenates 2+ .pdf files')
@click.argument('pdf_list', nargs=-1, type=click.Path())
def pdf_concatenate(pdf_list):
  """
  Concatenates list of input .pdf files into a new concatenated .pdf file
  """
  try:
    assert len(pdf_list) > 1
    for file in pdf_list:
      assert file.split(".")[1] == 'pdf'
      assert os.path.isfile(file)
  except:
    print('Please use 2+ <filename.pdf> files as an argument')
    sys.exit()

  merger = PyPDF2.PdfMerger()
  for file in pdf_list:
    merger.append(file)

  filename = 'concatenated.pdf'
  merger.write(filename)
  print(f'New file {filename} created')

  merger.close()


@cli.command(name='merge', help='args: 2+ tuples of (position to insert, .pdf file, pages (start, stop[, step]))')
@click.argument('pdf_tuples', nargs=-1)
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
    print('Please use tuples: (position to insert [0:], <filename.pdf>, (start, stop[, step])) as arguments')
    sys.exit()

  merger = PyPDF2.PdfMerger()
  for tuple in pdf_tuples:
    merger.merge(position=tuple[0], fileobj=tuple[1], pages=tuple[2])

  filename = 'merged.pdf'
  merger.write(filename)
  print(f'New file {filename} created')

  merger.close()


@cli.command(name='delete', help='args: .pdf file, pages seperated by a space')
@click.argument('pdf_file', nargs=1, type=click.Path())
@click.argument('pages_str', nargs=-1)
def pdf_delete(pdf_file, pages_str):
  """
  Delete pages from a .pdf file and save it to a new file
  """
  try:
    assert pdf_file.split(".")[1] == 'pdf'
    assert os.path.isfile(pdf_file)
  except:
    print('Please use <filename.pdf> as an argument')
    sys.exit()

  pages = []
  for i in pages_str:
    pages.append(int(i) - 1)

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
  cli()
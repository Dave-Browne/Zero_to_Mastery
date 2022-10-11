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
  Rotate the page in the file and save it to a new file
  """
  try:
    assert pdf_file.split(".")[1] == 'pdf'
    assert os.path.isfile(pdf_file)
  except:
    print('Please use <filename.pdf> as an argument')
    sys.exit()

  file = open(pdf_file, 'rb')
  reader = PyPDF2.PdfFileReader(file)
  writer = PyPDF2.PdfFileWriter()

  for page_num in range(reader.getNumPages()):
    current_page = reader.getPage(page_num)
    if page_num == (page - 1):
        for i in range(num_rotations):
          current_page.rotateClockwise(90)
    writer.addPage(current_page)

  filename = pdf_file.split(".")[0] + "_1.pdf"
  new_file = open(f'{filename}', 'wb')
  writer.write(new_file)
  print(f'New file {filename} created')

  file.close()
  new_file.close()

@cli.command(name='merge', help='args: 2+ .pdf files')
@click.argument('pdf_list', nargs=-1, type=click.Path())
def pdf_combiner(pdf_list):
  """
  Merge list of input pdf files into a new merged pdf file
  """
  try:
    assert len(pdf_list) > 1
    for file in pdf_list:
      assert file.split(".")[1] == 'pdf'
      assert os.path.isfile(file)
  except:
    print('Please use 2+ <filename.pdf> files as an argument')
    sys.exit()

  merger = PyPDF2.PdfFileMerger()
  for file in pdf_list:
    merger.append(file)

  merger.write('merged.pdf')
  print(f'New file "merged.pdf" created')
  merger.close()


if __name__ == '__main__':
  cli()

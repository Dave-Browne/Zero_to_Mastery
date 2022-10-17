#!/usr/bin/env python3

import PyPDF2
import sys
import os.path
import argparse


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
  
def pdf_rotateCW_90(pdf_file, pages_str_list, num_rotations_str_list=1):
  """
  Rotate a page 90deg clockwise in a .pdf file and save it to a new file
  Rotate multiple pages by making a list, eg python pdf.py -r test.pdf [1,2,3] [2,2,1]
  args: ['test.pdf', '[1,2,3]', '[2,2,1]']
  """
  # Process user input
  pages = []
  num_rotations = []
  disallowed_chars = '[] '

  try:
    for ch in disallowed_chars:
      pages_str_list = pages_str_list.replace(ch, "")
      num_rotations_str_list = num_rotations_str_list.replace(ch, "")
    pages_str_list = pages_str_list.split(",")
    num_rotations_str_list = num_rotations_str_list.split(",")
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

def pdf_merge(pdf_input_data):
  """
  Weld pdf files together and save it to a new file
  eg python pdf.py -m [a.pdf, 1, 5] [b.pdf, 1, 3] [a.pdf, 6, 10] [c.pdf, 2, 3]
  args: ['[a.pdf, 1, 5]', '[b.pdf, 1, 3]', '[a.pdf, 6, 10]', '[c.pdf, 2, 3]']
  """
  # Process user input
  pdf_data = []
  data = []
  disallowed_chars = '[] '

  print(f'pdf_input_data {pdf_input_data}')
  try:
    for input_data in pdf_input_data:
      for ch in disallowed_chars:
        input_data = input_data.replace(ch, "")                   # ['a.pdf,1,5']
      print(f'input_data_nochar {input_data}')
      input_data = input_data.split(",")                          # ['a.pdf','1','5']
      print(f'input_data_split  {input_data}')

      # Temporarily use 0 as a placemarker PdfMerger insert page
      pdf_data.append([0, input_data[0], int(input_data[1])-1, int(input_data[2])-1])       # [[0,'a.pdf',0,4], [0,'b.pdf',0,2], [0,'a.pdf',5,9], [0,'c.pdf',1,2]]
      print(f'data_corrected--- {pdf_data}')
    
      assert pdf_data[1].split(".")[1] == 'pdf'
      assert os.path.isfile(pdf_data[1])
  except:
    print('Use [<filename.pdf> pg_start pg_stop] [<filename.pdf> pg_start pg_stop] as arguments')
    sys.exit()

  merger = PyPDF2.PdfMerger()

  # Calculate the insert page pdf_data[1:][0] for the PdfMerger
  for i in range(1, len(pdf_data)):
    pdf_data[i][0] = pdf_data[i-1][0] + pdf_data[i-1][3] - pdf_data[i-1][2] + 1             # [[0,'a.pdf',0,4], [5,'b.pdf',0,2], [8,'a.pdf',5,9], [13,'c.pdf',1,2]]
  print(f'pdf_data_insert_pos {pdf_data}')
      
  # Create a tuple of (start, stop) page for the PdfMerger
  for i in range(len(pdf_data)):
    pdf_data[i][2] = tuple(pdf_data[i][2], pdf_data[i][3])
    del pdf_data[i][3]                                            # [[0,'a.pdf',(0,4)], [5,'b.pdf',(0,2)], [8,'a.pdf',(5,9)], [13,'c.pdf',(1,2)]]
    
    merger.merge(position=pdf_data[i][0], fileobj=pdf_data[i][1], pages=pdf_data[i][2])

  print(f'pdf_data_tuple {pdf_data}')

  filename = 'merged.pdf'
  merger.write(filename)
  print(f'New file {filename} created')

  merger.close()


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Manipulate .pdf files")
  group = parser.add_mutually_exclusive_group()
  group.add_argument('-c', '--concatenate', nargs='+', metavar='FILENAME.PDF')
  group.add_argument('-d', '--delete', nargs='+', metavar=('FILENAME.PDF', 'PAGE'))
  group.add_argument('-r', '--rotate', nargs=3, metavar=('FILENAME.PDF', '[PAGES]', '[NUM_ROTATIONS_CW_90DEG]'), help = 'eg python pdf.py -r test.pdf [1,2,3] [2,2,1]')
  group.add_argument('-m', '--merge', nargs=4, action='append', metavar=('PG_INSERT', 'FILENAME.PDF', 'PG_START', 'PG_STOP', help='python pdf.py -m [a.pdf, 1, 5] [b.pdf, 1, 3] [a.pdf, 6, 10] [c.pdf, 2, 3]'))

  args = parser.parse_args()

  if args.concatenate:
    pdf_concatenate(args.concatenate)
  elif args.delete:
    pdf_delete(args.delete[0], args.delete[1:])
  elif args.rotate:
    pdf_rotateCW_90(args.rotate[0], args.rotate[1], args.rotate[2])
  elif args.merge:
    pdf_merge(args.merge)

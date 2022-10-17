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
    for pdf_file in pdf_list:
      assert '.' in pdf_file
      assert pdf_file.split(".")[1] == 'pdf'
      assert os.path.isfile(pdf_file)
  except AssertionError:
    print('Use 2+ <filename.pdf> files as arguments')
    sys.exit()

  merger = PyPDF2.PdfMerger()
  for pdf_file in pdf_list:
    merger.append(pdf_file)

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
    assert '.' in pdf_file
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
  
def pdf_rotateCW_90(pdf_file, pages_str_list, num_rotations_str_list):
  """
  Rotate a page 90deg clockwise in a .pdf file and save it to a new file
  Rotate multiple pages by making a list, eg python pdf.py -r test.pdf "1,2,3" "2,2,1"
  args: ['test.pdf', '1,2,3', '2,2,1']
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
    assert '.' in pdf_file
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
    print('Use <filename.pdf> "pages" "num_rotations" as arguments')
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
  eg python pdf.py -m "a.pdf, 1, 5" "b.pdf, 1, 3" "a.pdf, 6, 10" "c.pdf, 2, 3"
  args: ['a.pdf 1 5', 'b.pdf 1 3', 'a.pdf 6 10', 'c.pdf 2 3']
  """
  # Process user input
  pdf_data = []
  data = []
  disallowed_chars = '[]'
  counter = 0

  try:
    for input_data in pdf_input_data:
      for ch in disallowed_chars:
        input_data = input_data.replace(ch, "")
      input_data = input_data.split(" ")                                                    # ['a.pdf', '1', '5']

      # Temporarily use 0 as a placemarker for PdfMerger insert page argument
      # Stop value is not included in merger so don't deduct 1
      pdf_data.append([0, input_data[0], int(input_data[1])-1, int(input_data[2])])         # [[0,'a.pdf',0,5], [0,'b.pdf',0,3], [0,'a.pdf',5,10], [0,'c.pdf',1,3]]
    
      assert '.' in pdf_data[counter][1]
      assert pdf_data[counter][1].split(".")[1] == 'pdf'
      assert os.path.isfile(pdf_data[counter][1])
      counter += 1
  except:
    print('Use at least 2 args like "<filename.pdf> pg_start pg_stop" "<filename.pdf> pg_start pg_stop"')
    sys.exit()

  merger = PyPDF2.PdfMerger()

  # Calculate the insert page pdf_data[1:][0] for the PdfMerger
  for i in range(1, len(pdf_data)):
    pdf_data[i][0] = pdf_data[i-1][0] + pdf_data[i-1][3] - pdf_data[i-1][2] + 1             # [[0,'a.pdf',0,4], [5,'b.pdf',0,2], [8,'a.pdf',5,9], [13,'c.pdf',1,2]]
      
  # Create a tuple of (start, stop) page for the PdfMerger
  for i in range(len(pdf_data)):
    pdf_data[i][2] = (pdf_data[i][2], pdf_data[i][3])
    del pdf_data[i][3]                                                                      # [[0,'a.pdf',(0,4)], [5,'b.pdf',(0,2)], [8,'a.pdf',(5,9)], [13,'c.pdf',(1,2)]]
    
    merger.merge(position=pdf_data[i][0], fileobj=pdf_data[i][1], pages=pdf_data[i][2])

  filename = 'merged.pdf'
  merger.write(filename)
  print(f'New file {filename} created')

  merger.close()


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Manipulate .pdf files")
  group = parser.add_mutually_exclusive_group()
  group.add_argument('-c', nargs='+', metavar='FILENAME.PDF', help = 'CONCATENATE eg python pdf.py -c a.pdf b.pdf c.pdf')
  group.add_argument('-d', nargs='+', metavar=('FILENAME.PDF', 'PAGE'), help = 'DELETE eg python pdf.py -d a.pdf 2 3 5')
  group.add_argument('-r', nargs=3, metavar=('FILENAME.PDF', '[PAGES]', '[NUM_ROTATIONS_CW_90DEG]'), help = 'ROTATE eg python pdf.py -r test.pdf "1,2,3" "2,2,1"')
  group.add_argument('-m', nargs=3, action='append', metavar=('FILENAME.PDF', 'PG_START', 'PG_STOP'), help = 'MERGE eg python pdf.py -m "a.pdf, 1, 5" "b.pdf, 1, 3" "a.pdf, 6, 10" "c.pdf, 2, 3"')

  args = parser.parse_args()

  if args.c:
    pdf_concatenate(args.c)
  elif args.d:
    pdf_delete(args.d[0], args.d[1:])
  elif args.r:
    pdf_rotateCW_90(args.r[0], args.r[1], args.r[2])
  elif args.m:
    pdf_merge(args.m[0])

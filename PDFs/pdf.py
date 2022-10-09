import PyPDF2
import sys


def pdf_rotateCW_90(pdf_file, page=1, num_rotations=1):
  """
  Rotate the page in the file and save it to a new file
  """
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

def pdf_combiner(pdf_list):
  """
  Merge list of input pdf files into a new merged pdf file
  """
  merger = PyPDF2.PdfFileMerger()
  for pdf in pdf_list:
    merger.append(pdf)

  merger.write('merged_pdf.pdf')
  print(f'New file "merged.pdf" created')
  merger.close()


if __name__ == '__main__':
  if len(sys.argv) == 1:
    print(f'*******************************************************************')
    print(f'Purpose: To merge pdf\'s or rotate pages in them')
    print(f'merge args : 2+ file names (include .pdf) to merge in sequential order')
    print(f'rotate args: one file name (include .pdf)')
    print(f'             page num to rotate (default=1)')
    print(f'             number of times to rotate 90deg clockwise (default=1)')
    print(f'*******************************************************************')
    sys.exit()

  inputs = sys.argv[1:]

  choice = input("Type 'merge' or 'rotate': ")
  if choice == 'merge':
    try:
      for i in range(len(inputs)):
        assert isinstance(inputs[i], str)
      if len(inputs) > 1:
        pdf_combiner(inputs)
    except:
      print(f'run program with no args to see help')
  elif choice == 'rotate':
    try:
      assert isinstance(inputs[0], str)

    except:
      print(f'run program with no args to see help')

    if len(inputs) == 1:
      pdf_rotateCW_90(pdf_file=inputs[0])
    elif len(inputs) == 2:
      pdf_rotateCW_90(pdf_file=inputs[0], page=int(inputs[1]))
    elif len(inputs) == 3:
      pdf_rotateCW_90(pdf_file=inputs[0], page=int(inputs[1]), num_rotations=int(inputs[2]))

  else:
    sys.exit()
    
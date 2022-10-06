import PyPDF2

def rotateCW_90(doc, page=0, no_rotations=1):
  file = open(doc, 'rb')
  reader = PyPDF2.PdfFileReader(file)
  pg = reader.getPage(page)
  for i in range(no_rotations):
    pg.rotateCounterClockwise(90)

  writer = PyPDF2.PdfFileWriter()
  writer.addPage(pg)
  new_file = open('rotated.pdf', 'wb')
  writer.write(new_file)

if __name__ == '__main__':
  rotateCW_90('twopage.pdf', 1, 2)
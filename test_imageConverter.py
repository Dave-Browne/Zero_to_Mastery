import unittest
import JPEGtoPNGconverter

class TestConverter(unittest.TestCase):
  def test_oneArg(self):
    arg1 = 'ímages/'
    arg2 = ''
    result = JPEGtoPNGconverter.converter(arg1, arg2)
    self.assertFalse(result)

  def test_noSlash(self):
    arg1 = 'ímages/'
    arg2 = 'new_img'
    result = JPEGtoPNGconverter.converter(arg1, arg2)
    self.assertFalse(result)

  def test_wrongType(self):
    arg1 = 1
    arg2 = 'new_imgs'
    result = JPEGtoPNGconverter.converter(arg1, arg2)
    self.assertFalse(result)

  def test_wrongJPEGdir(self):
    arg1 = 'foobar/'
    arg2 = 'new_imgs/'
    result = JPEGtoPNGconverter.converter(arg1, arg2)
    self.assertFalse(result)


if __name__ == '__main__':
  unittest.main()
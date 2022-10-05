import unittest
import guessNumber

class TestGame(unittest.TestCase):
  def test_correct_guess(self):
    test_answer = 5
    test_guess = 5
    result = guessNumber.guessing_game(test_answer, test_guess)
    self.assertTrue(result)

  def test_incorrect_guess(self):
    test_answer = 7
    test_guess = 3
    result = guessNumber.guessing_game(test_answer, test_guess)
    self.assertFalse(result)

  def test_outside_range(self):
    test_answer = 5
    test_guess = 11
    result = guessNumber.guessing_game(test_answer, test_guess)
    self.assertFalse(result)

  def test_string(self):
    test_answer = 5
    test_guess = 'hello'
    result = guessNumber.guessing_game(test_answer, test_guess)
    self.assertFalse(result)

if __name__ == '__main__':
  unittest.main()
import random

def guessing_game(answer, guess):  
      if (isinstance(guess, int)) and (0 < guess < 11):
        if guess == answer:
          print('You\'re a genius!!!')
          return True
      else:
        print('hey bozo, I said 1~10')
        return False

if __name__ == '__main__':
  random_number = random.randint(1, 10)
  while True:
    try:
      guess = int(input('guess a number 1~10: '))
      if guessing_game(random_number, guess):
        break

    except ValueError:
      print('Please enter a number... ')
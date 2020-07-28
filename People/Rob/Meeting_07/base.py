# A plan for the objects and methods for PyQuizmaster 2

from collections.abc import Iterable

class QuizItem:
    """
    The QuizItem Class. This class will hold attributes of
    a vocab word and its description.
    """

    __slots__ = ('word', 'answer')
    
    def __init__(self):
        self.word = 'temp'
        self.answer = 'temp'

    # Set the word and answer using the property decorator
    

class Deck(Iterable):
    """
    The Deck Class. This class will be the main data structure
    for the flashcards. It will hold instances of the QuizItem
    class in a list and allow the user to cycle through and 
    shuffle the QuizItems.
    """
    def __init__(self):
        self.items = []

    def shuffle(self):
        pass

    

class Quizzer:
    """
    The Quizzer Class. This class will manage the deck and 
    track correct and incorrect answers.
    """
    def __init__(self):
        self.num_correct = 0
        self.num_wrong = 0

    def check_correct(quiz_item, choice):
        if not isinstance(quiz_item, QuizItem):
            raise TypeError
        
        if quiz_item.answer == choice:
            return True
        else:
            return False

class Interface:
    """
    Defines the methods for interacting with the user
    through a Graphic User Interface (GUI).
    """

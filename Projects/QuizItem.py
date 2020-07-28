# The QuizItem Class

import datetime

class QuizItem:
    """
    The QuizItem Class. This class will hold attributes of
    a vocab word and its description.
    """

    #__slots__ = ('word', 'answer', '__date_created', 'date_editted')
    
    def __init__(self, word, answer, date_created=None, date_editted=None):
        self.word = word
        self.answer = answer
        self.__date_created = date_created if date_created is not None else datetime.datetime.now()
        self.date_editted = date_editted if date_editted is not None else datetime.datetime.now()

    @property
    def date_created(self):
        return self.__date_created

    @property
    def date_editted(self):
        return self.__date_editted

    @date_editted.setter
    def date_editted(self, value):
        if not isinstance(datetime.datetime, value):
            raise TypeError
        else:
            self.__date_editted = value


        
    # Set the word and answer using the property decorator


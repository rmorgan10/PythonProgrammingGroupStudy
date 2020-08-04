# The QuizItem Class

import datetime


class QuizItem:
    """
    The QuizItem Class. This class will hold attributes of
    a vocab word and its description.
    
    Any new attributes of an inheriting class must be sortable (have a defined comparison operator)
    """

    __slots__ = ('__word', '__answer', '__date_created', '__date_edited', '__difficulty')
    
    def __init__(self, word, answer, difficulty=0, date_created=None, date_edited=None):
        self.__date_created = date_created if date_created is not None else datetime.datetime.now()
        self.date_edited = date_edited if date_edited is not None else datetime.datetime.now()

        self.word = word
        self.answer = answer
        self.__difficulty = difficulty

    @property
    def difficulty(self):
        return self.__difficulty

    @property
    def word(self):
        return self.__word

    @word.setter
    def word(self, new_word):
        if not isinstance(new_word, str):
            raise TypeError("U DUmboo, Wowww I cannot workd in an environment with that kind of "
                            "h*te speach just thrown around. Los*r")
        self.date_edited = datetime.datetime.now()
        self.__word = new_word

    @property
    def answer(self):
        return self.__answer

    @answer.setter
    def answer(self, new_answer):
        if not isinstance(new_answer, str):
            raise TypeError("U DUmboo, Wowww I cannot workd in an environment with that kind of "
                            "h*te speach just thrown around. Los*r")
        self.date_edited = datetime.datetime.now()
        self.__answer = new_answer

    @property
    def date_created(self):
        return self.__date_created

    @property
    def date_edited(self):
        return self.__date_edited

    @date_edited.setter
    def date_edited(self, value):
        if not isinstance(value, datetime.datetime):
            raise TypeError("No u dummy this is soposed to be a date"
                            " loos*r")
        else:
            self.__date_edited = value

    def update_difficulty(self, correct: bool):
        self.__difficulty += int(not correct)
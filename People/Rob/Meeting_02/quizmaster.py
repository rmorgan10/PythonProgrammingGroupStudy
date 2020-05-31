# An interactive quiz of python builtins

import pyfiglet
import random
import textwrap
import time

class Quiz():
    """
    An interactive quiz of python builtins
    """
    def __init__(self, keywords=None, definitions=None):
        """
        Make a mapping of keywords to definitions and start quiz.

        :param keywords: array-like, keywords for quiz
        :param definitions: array-like, definitions for quiz
        """
        # Use pyfiglet for ascii displays
        self.fig = pyfiglet.Figlet(font='standard')
        self._store_art()
        
        if keywords is None:
            # No keywords specified, so use all
            self.quiz_info = {x: eval(x).__doc__ for x in dir(__builtins__)}
            self._insert_missing_docs()

        if keywords is not None and definitions is not None:
            # Make a dictionary from specified keywords
            self.quiz_info = {k: d for k, d in zip(keywords, definitions)}

            # Notify user if zip will truncate a list
            if len(keywords) != len(definitions):
                print("Warning: You supplied {0} keywords and {1} definitions.".format(keywords, definitions))
                print("         The supplied lists will be truncated.")

        # Exit if keywords and definitions were incorrectly supplied
        if not hasattr(self, "quiz_info"):
            print("You must supply definitions if you supply keywords.")
            exit()
            
        self.start()
        return

    def _insert_missing_docs(self):
        """
        Some of the python builtins have 'None' for their __doc__. Fill in
        the mssing values here.
        """
        missing = ["Ellipsis", "None", "NotImplemented", "__doc__",
                   "__name__", "__package__", "__spec__", "exit", "quit"]

        defs = ["A index slicing convention developed for NumPy arrays",
                "Shared reference to a null-space in memory",
                "Used to denote when certain arithatic operations do not" +
                "apply to a given data type",
                "The docstring of an object",
                "The name of the script that the interpreter is interpreting",
                "The name of the module from which something can be imported",
                "Set to a module name or 'None' if in interactive mode",
                "Prompt the user to exit the script",
                "Prompt the user to quit the script"]

        for m, d in zip(missing, defs):
            self.quiz_info[m] = d

        return

    def pose_question(self, keyword):
        """
        Ask user to select definition of specified keyword.
        
        :param keyword: str, name of python keyword for question
        :return: correct: bool, True if correct, False if wrong 
        """

        # Determine correct answer
        correct_answer = self.quiz_info[keyword]
        
        # Prevent correct answer from being used twice
        weights = [1 if d != correct_answer else 0 for d in self.quiz_info.values()]
        wrong_answers = random.choices(list(self.quiz_info.values()), weights=weights, k=3)
        wrong_iter = iter(wrong_answers)

        # Define answer choices as letters and randomly choose the correct answer
        shuffled_answers = ['a', 'b', 'c', 'd']
        answers = shuffled_answers[:]
        random.shuffle(shuffled_answers)
        correct_choice = shuffled_answers.pop()
        correct_idx = answers.index(correct_choice)

        print("\nSelect the correct definition of '{}'\n".format(keyword))
        for idx, ans in enumerate(answers):

            if idx == correct_idx:
                print("  " + ans + ')\t' + self._format_answer(correct_answer) + '\n')
            else:
                print("  " + ans + ')\t' + self._format_answer(next(wrong_iter)) + '\n')
        
        user_choice = input("Enter your selection: ").strip().lower()
        while user_choice not in answers:
            print("You must select from ['a', 'b', 'c', 'd']...")
            user_choice = input("Enter your selection: ").strip().lower()

        return user_choice == correct_choice


        
    def _format_answer(self, text):
        """
        Make the standard output look nice by wrapping text

        :param text: str, the text of a single answer to be formatted
        :return: pretty_text: str, formatted answer
        """
        text = str(text).replace('\n', ' ')
        answer_width = 70
        pretty_text = '\n\t'.join(textwrap.wrap(text, answer_width))

        return pretty_text

    def _format_score(self, correct, total):
        """
        Print the score in ascii art

        :param correct: int, the number of questions answered correctly
        :param total: int, the number of questions asked
        :return: score: ascii representation of the user's score
        """
        correct_ascii = self.fig.renderText(str(correct)).split('\n')
        total_ascii = self.fig.renderText(str(total)).split('\n')
        prefix = self.fig.renderText("Score: ").replace('\n', '   \n').split('\n')
        score = [w + x + y + z for w, x, y, z in zip(prefix, correct_ascii, self.slash.split('\n'), total_ascii)]

        return score

    def _format_question_break(self, name):
        """
        Return a header for a given question name

        :param num: str, the name of the question
        :return: header: str, formatted question header
        """
        header = '-' * 80 + '\n'
        buffer_length = int((80 - int(len(name))) / 2) 
        header += ' ' * buffer_length + name + ' ' * buffer_length + '\n'
        header += '-' * 80 + '\n'

        return header
        
        
    def _store_art(self):
        """
        Store ascii messages as object attributes.
        """
        self.correct = self.fig.renderText("CORRECT!")
        self.title = """
         ____        _   _                 
        |  _ \ _   _| |_| |__   ___  _ __  
        | |_) | | | | __| '_ \ / _ \| '_ \ 
        |  __/| |_| | |_| | | | (_) | | | |
        |_|    \__, |\__|_| |_|\___/|_| |_|
         ____  |___/ _     __  __           _            
        /  _ \ _   _(_)___|  \/  | __ _ ___| |_ ___ _ __ 
        | | | | | | | |_  / |\/| |/ _` / __| __/ _ \ '__|
        | |_| | |_| | |/ /| |  | | (_| \__ \ ||  __/ |   
        \__\_\ \__,_|_/___|_|  |_|\__,_|___/\__\___|_|   

        """
        self.incorrect = """
         _   _                              __
        | \ | | ___  _ __   ___      _     / /
        |  \| |/ _ \| '_ \ / _ \    (_)   / / 
        | |\  | (_) | |_) |  __/     _   / /  
        |_| \_|\___/| .__/ \___|    (_) /_/   
                    |_|                    
        """
        self.slash = self.fig.renderText("/")

        return

    def start(self, num_questions=10):
        """
        Run the quiz and keep score.

        :param num_questions: int, number of questions in quiz
        """
        # Display some art
        print(self.title)

        # Order keywords randomly
        keywords = list(self.quiz_info.keys())
        random.shuffle(keywords)

        # Run the quiz
        num_correct = 0
        for question_num in range(1, int(num_questions) + 1):

            # Add a delay so user can read output
            time.sleep(1.5)
            
            # Display header
            question_header = self._format_question_break("Question " + str(question_num))
            print(question_header)

            # Choose the keyword for the question
            keyword = keywords.pop()
            correct = self.pose_question(keyword)

            # Evaluate user response
            if correct:
                # Notify user that they were correct
                num_correct += 1
                print(self.correct)

            else:
                # Notify user that they were incorrect
                print(self.incorrect)
                print("The correct answer was:\n")
                print('\t' + self._format_answer(self.quiz_info[keyword]))
                
        # Display quiz score
        print("\n")
        time.sleep(1.5)
        msg = "Calculating Results"
        for _ in range(4):
            print(msg, end='\r')
            msg += '.'
            time.sleep(1)
        print('\n')
        score = self._format_score(num_correct, num_questions)
        print('\n'.join(score))

if __name__ == "__main__":
    q = Quiz()

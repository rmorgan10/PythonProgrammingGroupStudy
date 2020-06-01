#!/usr/bin/env python3

from datetime import datetime
import pytz
from random import choice
from typing import List, Tuple, Dict
import os


def build_dict(f_name: str) -> Dict[str, str]:
	"""
	builds a dictionary mapping builtins to their descriptions from the passed
	in file.

	Args:
		f_name : name of file containing descriptions of builitins

	Returns:
		dict{str: str}:
			maps builtins to their descriptions
	"""
	desc_dict = {}
	lens = []
	with open(f_name, "r") as descriptions:
		for i, line in enumerate(descriptions):
			# print(f"line {i} : {line}")
			ln_1, ln_2 = line.split(" : ")
			ln_2 = ln_2.replace("\n", "")
			desc_dict.update({ln_1: ln_2})
	return desc_dict


def quiz(des_dict: Dict[str, str], ques: int = 10, prompt_desc: bool = True, passing: float = .8):
	"""
	Function should pop up a new terminal which formats a quiz, asking the player
	to select from four options (A, B, C, or D).
	The prompt should ask the player
	to match the provided description (or builtin) with the four available builtins
	(or descriptions).
	The player should be able to select any options by typing in A B C or D into
	the terminal. If the player provides a string longer than one character, every
	character in that string is evaluated sequentially as an answer to the following
	questions. Inputs other than A B C or D are registered as incorrect.
	Should be insensitive to case.
	Once all of the questions have been answered the quiz gives the player their
	score and either complements them or berates them.
	"""
	# determine if it's June:
	if is_it_june():
		pride_month()
	else:
		corporate()

	options = ['A', 'B', 'C', 'D']
	user_answers = ""
	right_answers = ""
	for i in range(ques):
		correct, bltin, desc, prompt, responses = set_q_texts(
			des_dict,
			prompt_desc,
			options
		)
		right_answers += correct
		question = f"Question {i+1} : {prompt}\n"
		for key, value in responses.items():
			question += f"{key}) {value}\n"
		question += f"Your answer? :"
		if len(user_answers) < i+1:
			user_answers += input(question).upper()
		else:
			print(question)
		user_response = user_answers[i]
		user_msg = ("Good Job!" if user_response == correct else "Okay Job.")
		try:
			print(
				f"""\nYou answered {user_response}: {responses[user_response]}
correct answer was {correct}: {responses[correct]}
{user_msg}\n"""
			)
		except KeyError:
			print(f"""What? Why would you answer {user_response}?? That's not
even an option. Well now you got it wrong! And look at what you did
""")
		input("press any key to continue")
		os.system('cls')
	tot_correct = sum(usr == cor for usr, cor in zip(user_answers, right_answers))
	master = "You are a PyMaster!"
	padawan = "You have much to learn young Pydawan."
	usr_is = master if tot_correct > ques*passing else padawan
	usr_is = "You complete buffoon!" if tot_correct == 0 else usr_is
	print(f"You got {tot_correct} out of {ques} questions right.\n{usr_is}")


def set_q_texts(
		des_dict: dict,
		prompt_desc: bool,
		options: List[str]
) -> Tuple[str, str, str, str, Dict[str, str]]:
	"""

	Args:
		des_dict ():
		ques ():
		prompt_desc ():
		options ():

	Returns:

	"""
	correct = choice(options)
	bltin = choice(list(des_dict.keys()))
	desc = des_dict[bltin]
	responses = {}
	# set the prompt and responses variables
	if prompt_desc:
		prompt = desc
		for option in options:
			if option == correct:
				responses[option] = bltin
			else:
				responses[option] = choice(
					list(filter(
						lambda l: l != bltin,
						des_dict.keys()
					))
				)
	else:
		prompt = bltin
		for option in options:
			if option == correct:
				responses[option] = bltin
			else:
				responses[option] = choice(
					filter(
						lambda l: l != desc,
						des_dict.values()
					)
				)
	return correct, bltin, desc, prompt, responses


def corporate():
	"""
	Formats the terminal to use browns
	"""
	pass


def pride_month():
	"""
	Formats terminal to use very pretty colors
	"""
	pass


def is_it_june() -> bool:
	"""
	determines if it is currently June in Madison, Wisconsin
	Returns:
		True if it is June, False otherwise
	"""
	tz = pytz.timezone("US/Central")
	the_now = datetime.now(tz)
	return datetime.date(the_now).month == 6


if __name__ == '__main__':
	descriptions = build_dict("builtins.txt")
	quiz(descriptions, ques=3)


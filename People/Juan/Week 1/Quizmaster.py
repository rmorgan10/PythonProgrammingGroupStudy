#!/usr/bin/env python3

from datetime import datetime
import pytz
from random import choice
from typing import List, Tuple, Dict
import os
import time


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
			ln_1, ln_2 = line.split(" : ")
			ln_2 = ln_2.replace("\n", "")
			desc_dict.update({ln_1: ln_2})
	return desc_dict


def format_the_rainbow(message: str) -> str:
	"""
	Formats the message with escape sequences to make it very pretty on the output
	Args:
		message : string to be formatted

	Returns:
		rainbow-fied message
	"""

	# format is "\033[1;<text_color_code>;<background_color_code>m <text>"
	# Text colors
	t_black = "30"
	t_red = "31"
	t_green = "32"
	t_yellow = "33"
	t_blue = "34"
	t_purple = "35"
	t_cyan = "36"
	t_white = "37"

	# background colors
	b_red = f"{31+10}"
	b_green = f"{32+10}"
	b_yellow = f"{33+10}"
	b_blue = f"{34+10}"
	b_purple = f"{35+10}"
	b_cyan = f"{36+10}"
	b_white = f"{37+10}"

	t_rainbow = [t_red, t_yellow, t_green, t_blue, t_purple]
	b_rainbow = [b_red, b_yellow, b_green, b_blue, b_purple]
	rain_l = len(t_rainbow)

	g_message = ""
	shift = 2
	start = choice(range(rain_l))
	for i, slc in enumerate(message.split("\n")):
		col = t_rainbow[(i+start) % rain_l]
		bg = b_rainbow[(i+start+shift) % rain_l]
		g_message += f"\033[1;{col};{bg}m {slc}\n"
	return g_message[:-2] + "\033[0m"


def formatted_for_synergy(message: str) -> str:
	"""
	Formats the message with very tasteful and professional blacks whites and browns
	Args:
		message : string to be formatted

	Returns:
		synergistic message
	"""
	# format is "\033[1;<text_color_code>;<background_color_code>m <text>"
	# Text colors
	t_black = "30"
	t_red = "31"
	t_green = "32"
	t_yellow = "33"
	t_blue = "34"
	t_purple = "35"
	t_cyan = "36"
	t_white = "37"

	# background colors
	b_black = f"{30+10}"
	b_red = f"{31+10}"
	b_green = f"{32+10}"
	b_yellow = f"{33+10}"
	b_blue = f"{34+10}"
	b_purple = f"{35+10}"
	b_cyan = f"{36+10}"
	b_white = f"{37+10}"

	t_dwight = [t_yellow, t_white]
	b_dwight = [b_black, b_blue]
	rain_l = len(t_dwight)

	g_message = ""
	shift = 2
	start = choice(range(rain_l))
	for i, slc in enumerate(message.split("\n")):
		col = t_dwight[(i+start) % rain_l]
		bg = b_dwight[(i+start+shift) % rain_l]
		g_message += f"\033[1;{col};{bg}m {slc}\n"
	return g_message[:-2] + "\033[0m"


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
		formatter = format_the_rainbow
	else:
		formatter = formatted_for_synergy
	print_c = lambda ms: print(formatter(ms))
	input_c = lambda ms: input(formatter(ms))

	print_c("Empty Message to set formatting")
	os.system('cls')
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
			user_answers += input_c(question).upper()
		else:
			print_c(question)
		user_response = user_answers[i]
		user_msg = ("Good Job!" if user_response == correct else "Okay Job.")
		try:
			print_c(
				f"""\nYou answered {user_response}: {responses[user_response]}
correct answer was {correct}: {responses[correct]}
{user_msg}\n"""
			)
		except KeyError:
			print_c(f"""What? {user_response} isn't an option... I'm just gonna mark
this as wrong""")
		input_c("Hit enter/return to continue")
		os.system('cls')
	tot_correct = sum(usr == cor for usr, cor in zip(user_answers, right_answers))
	if tot_correct == 0:
		usr_is = "You must realize you are doomed."
	elif tot_correct < ques*passing:
		usr_is = "You have much to learn young Pydawan."
	else:
		usr_is = "You are a jedPy Master!"
	print_c(f"You got {tot_correct} out of {ques} questions right.\n{usr_is}")


def set_q_texts(
		des_dict: Dict[str, str],
		prompt_desc: bool,
		options: List[str]
) -> Tuple[str, str, str, str, Dict[str, str]]:
	"""
	Randomly chooses the correct answer to the question and creates a dictionary
	of options for the quiz taker.
	Args:
		des_dict : Dictionary of descriptions of python builtins
		prompt_desc : If true the description of the correct builtin is set as the
			prompt for the question and the builtins are the answer choises. Otherwise
			the roles are reversed
		options : List of len()=1 str which make up the potential answers

	Returns:
		(correct, bltin, desc, prompt, responses)
			correct: member of options that is the right answer
			bltin: builtin name which was chosen to be the right answer
			desc: the description related to bltin
			promp: the string prompt for the question
			responses: dictionary mapping options to builtin names or descriptions
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


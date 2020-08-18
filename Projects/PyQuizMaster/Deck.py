"""
Collection class for QuizItems
"""

from collections.abc import Iterable
from typing import Iterator, List, Union

from QuizItem import QuizItem

import pandas as pd
import os


class Deck(Iterable):

	def __init__(self, cards: List[QuizItem] = None, load_item: bool = True):
		self.cards: List[QuizItem] = [] if cards is None else cards
		if load_item:
			self.load() 

	def __iter__(self) -> Iterator:
		return self.cards.__iter__()

	def affix(self, new_card: QuizItem):
		if not isinstance(new_card, QuizItem):
			raise TypeError("only QuizItems can be added to the deck")
		self.cards.append(new_card)

	def sort_by(self, attribute: str, reverse: bool = False, in_place: bool = True):
		"""
		Sorts our deck by attribute. Stable.
		Args:
			attribute : attribute of our QuizItems over which we sort
			reverse : if True, sorts descending order, otherwise in ascending
				order
			in_place : should the deck be sorted in place.

		Returns:
			Either None, or a new, sorted, Deck object if in_place is true or false
		"""
		if not all([hasattr(card, attribute) for card in self.cards]):
			raise RuntimeWarning(
				f"I don't have this attribute '{attribute}', dumbo. List not sorted"
			)
			return self

		if in_place:
			self.cards.sort(
				key=lambda card: getattr(card, attribute),
				reverse=reverse
			)
			return self
		else:
			return Deck(sorted(
				self.cards,
				key=lambda card: getattr(card, attribute),
				reverse=reverse
			))
        
	def load(self):
		"""
		Load cards from CSV File as pandas dataframe
		Columns: word, answer, Date created, date edited, difficulty 
		"""
		file = "generic_file_name.csv"
		if os.path.exists(file):
			df = pd.read_csv(file, delimiter='~')
			for index, row in df.iterrows():
				self.affix(QuizItem(**dict(row)))
    
	def save(self):
		"""
		Save cards to CSV File
		"""
		file = "generic_file_name.csv"
		dict_to_save = {slot.replace("__",""):[] for slot in QuizItem.__slots__}
		for card in self.cards: 
			for key in dict_to_save.keys():
				dict_to_save[key].append(getattr(card, key))
		df = pd.DataFrame(dict_to_save, delimiter='~')
		df.to_csv(file, index=False)
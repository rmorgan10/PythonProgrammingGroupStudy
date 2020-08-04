"""
Collection class for QuizItems
"""

from collections.abc import Iterable
from typing import Iterator, _T_co, List, Union

from QuizItem import QuizItem


class Deck(Iterable):

	def __init__(self, cards: List[QuizItem] = None):
		self.cards: List[QuizItem] = [] if cards is None else cards
		# pass

	def __iter__(self) -> Iterator[_T_co]:
		pass

	def affix(self, new_card: QuizItem):
		if not isinstance(new_card, QuizItem):
			raise TypeError("only QuizItems can be added to the deck")
		self.cards.append(new_card)

	def sort_by_words(self):
		pass

	def sort_by(self, attribute: str, reverse: bool, in_place: bool) :
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
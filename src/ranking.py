import logging
import numpy as np
from random import shuffle
from copy import copy


class RankedSet:

	# Set of driver IDs (IN ORDER)
	_data: list[int]
	_relations: np.ndarray
	score: int

	def __init__(self, data: list[int], relations):
		self._data = data
		self._total_participants = len(self._data)
		self._relations = relations

		self.score = 0
		self.calculate_score()

	def calculate_score(self) -> None:
		tmp_score = 0

		# TODO: This is not the most efficient method to calculate score, update if we have time
		for driver_a_index, driver_a_id in enumerate(self._data):
			for driver_b_index in range(driver_a_index, self._total_participants):
				driver_b_id = self._data[driver_b_index]
				# logging.debug(f'{driver_a_index=}\t{driver_a_id=}\t{driver_b_index=}\t{driver_b_id=}')

				score = self._relations[driver_b_id, driver_a_id]
				if score > 0:
					tmp_score += score

		self.score = tmp_score

	def get_rankings(self) -> list[int]:
		return self._data

	def get_neighbour(self):
		# Change neighbourhood function here (debugging)
		return self._neighbourhood_swap()

	# Playing around with neighbourhood functions
	def _neighbourhood_shuffle(self):
		c = copy(self._data)
		shuffle(c)
		return RankedSet(c, self._relations)

	def _neighbourhood_shift(self, shift: int = 3):
		c = copy(self._data)
		new_data = c[shift:] + c[:shift]
		return RankedSet(new_data, self._relations)

	def _neighbourhood_swap(self):
		c = copy(self._data)

		# Create list of index
		id_list = list(range(int(len(c))))
		shuffle(id_list)

		# Swap two random items in the id list
		c[id_list[0]], c[id_list[1]] = c[id_list[1]], c[id_list[0]]

		return RankedSet(c, self._relations)

	def _neighbourhood_swap_multiple(self, swaps: int = 1):
		c = copy(self._data)

		# How many swaps to do
		for x in range(swaps):
			# Create list of index
			id_list = list(range(int(len(c))))
			shuffle(id_list)

			# Swap two random items in the id list
			c[id_list[0]], c[id_list[1]] = c[id_list[1]], c[id_list[0]]

		return RankedSet(c, self._relations)


if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(asctime)s - %(message)s')
	rs = RankedSet(list(range(1, 45)))

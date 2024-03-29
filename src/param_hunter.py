#!/usr/bin/python
import signal
from copy import copy
from contextlib import contextmanager
from sa import SimulatedAnnealing
from wmg import WMG


class TimeoutException(Exception): pass


@contextmanager
def time_limit(seconds):
	def signal_handler(signum, frame):
		raise TimeoutException("Timed out!")

	signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(seconds)
	try:
		yield
	finally:
		signal.alarm(0)


def run_sa(parser, test_initial_t, test_tl, test_num_non_improve, test_cooling, limit_func_time = 12):
	sa = SimulatedAnnealing(
		initial_t=test_initial_t,
		t_length=test_tl,
		num_non_improve=test_num_non_improve,
		cooling_ratio=test_cooling / 100
	)
	sa.set_wmg(parser)
	sa.initialise_rankings()

	hit_time_limit = False
	try:
		# Kill process if it takes longer than 3 seconds (stuck in num_non_improve)
		with time_limit(limit_func_time):
			sa.run_outer()
	except TimeoutException as e:
		print("Timed out!")
		hit_time_limit = True

	if hit_time_limit:
		return 99999, f'Timout {limit_func_time}s'

	return (sa.get_best_ranking().score, sa.get_execution_time())


def run_hunter() -> None:
	parser = WMG()
	parser.read_file('data/1994_Formula_One.wmg')
	parser.parse_file()

	REPLAY_COUNT = 10

	best_score = 749  # Initial solution
	current_params = [0, 0, 0, 0]
	best_params = [0, 0, 0, 0]

	for test_initial_t in range(5, 100, 2):
		print(f'- Iterated {test_initial_t=}')
		current_params[0] = test_initial_t
		for test_cooling in range(90, 99, 3):
			current_params[1] = test_cooling
			print(f'- Iterated {test_cooling=}')
			for test_tl in range(90, 150, 10):
				current_params[2] = test_tl
				print(f'- Iterated {test_tl=}')
				for test_num_non_improve in range(70, 150, 10):
					current_params[3] = test_num_non_improve
					print(f'- Iterated {test_num_non_improve=}')
					print(f'-Best score currently: {best_score}, with param set: {best_params}, testing params:{current_params}')

					score, time_str = run_sa(parser, test_initial_t, test_tl, test_num_non_improve, test_cooling, 10)

					if score <= best_score:
						param_replay = REPLAY_COUNT
						best_params = copy(current_params)
						best_score = score

						print(f'NEW BEST SCORE of {best_score} FOUND WITH PARAMS: {test_initial_t=}, {test_tl=}, {test_cooling=}, {test_num_non_improve=}')
						print(time_str)

						# If parameters are good, replay them to see if we get a better score
						while param_replay > 0:
							score, time_str = run_sa(parser, test_initial_t, test_tl, test_num_non_improve, test_cooling, 10)
							param_replay -= 1
							if score <= best_score:
								print(time_str)
								print(f'REPLAYING! {score} <= {best_score}')
								param_replay = REPLAY_COUNT
								best_score = score


if __name__ == '__main__':
	run_hunter()

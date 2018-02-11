import os

import matplotlib.pyplot as plt
import numpy as np
import pytest

from bank_sim import BankSimulation

sim = BankSimulation()


def test_lunch_break_distribution():
	dist = sim.get_lunch_break_distribution()

	x_range = np.linspace(0, 6, 1000)
	plt.plot(x_range, dist.pdf(x_range))
	plt.savefig(os.path.join("test_output", "lunch_break_dist.png"))
	plt.clf()

def test_transaction_time_distribution():
	dist = sim.get_transaction_time_distribution()

	x_range = np.linspace(-0.1, 0.5, 1000)
	plt.plot(x_range, dist.pdf(x_range))
	plt.savefig(os.path.join("test_output", "transaction_time_dist.png"))
	plt.clf()

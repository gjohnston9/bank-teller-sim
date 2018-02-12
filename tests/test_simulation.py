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


@pytest.mark.parametrize("t, plot_name", [
    (0, "no_rush"),
    (3, "rush"),
])
def test_intercustomer_arrival_time_distribution(t, plot_name):
	sim.t = t
	dist = sim.get_time_before_next_arrival_distribution()

	x_range = np.linspace(-0.2, 0.18, 1000)
	plt.plot(x_range, dist.pdf(x_range))
	plt.savefig(os.path.join("test_output", "intercustomer_arrival_time_dist_{}.png".format(plot_name)))
	plt.clf()
	sim.t = 0


@pytest.mark.parametrize("t, in_lunchtime", [
    (0, False),
    (2, False), # boundary case
    (3, True),
    (4, False), # boundary case
    (5, False),
])
def test_lunchtime(t, in_lunchtime):
	sim.t = t
	assert sim.in_lunchtime() == in_lunchtime
	sim.t = 0


@pytest.mark.parametrize("t, in_rush_period", [
    (0, False),
    (2, False), # boundary case
    (3, True),
    (4, False), # boundary case
    (5, False),
    (8, False), # boundary case
    (9, True),
    (10, False), # boundary case
    (11, False),
])
def test_rush_period(t, in_rush_period):
	sim.t = t
	assert sim.in_rush_period() == in_rush_period
	sim.t = 0


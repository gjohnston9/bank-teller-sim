import os

import matplotlib.pyplot as plt; plt.switch_backend('agg')
import numpy as np
import pytest

from bank_sim import BankSimulation

PLACEHOLDER_LUNCH_BREAK_LENGTH = 1
PLACEHOLDER_NUM_TELLERS = 2

@pytest.fixture()
def sim():
    return BankSimulation(PLACEHOLDER_LUNCH_BREAK_LENGTH, PLACEHOLDER_NUM_TELLERS)

def test_lunch_break_distribution(sim):
	dist = sim.get_lunch_break_distribution()

	x_range = np.linspace(0, 6, 1000)
	plt.plot(x_range, dist.pdf(x_range))
	plt.savefig(os.path.join("test_output", "lunch_break_dist.png"))
	plt.clf()


def test_transaction_time_distribution(sim):
	dist = sim.get_transaction_time_distribution()

	x_range = np.linspace(-0.1, 0.5, 1000)
	plt.plot(x_range, dist.pdf(x_range))
	plt.savefig(os.path.join("test_output", "transaction_time_dist.png"))
	plt.clf()


@pytest.mark.parametrize("t, plot_name", [
    (0, "no_rush"),
    (3, "rush"),
])
def test_intercustomer_arrival_time_distribution(sim, t, plot_name):
	sim.t = t
	dist = sim.get_time_before_next_arrival_distribution()

	x_range = np.linspace(-0.2, 0.18, 1000)
	plt.plot(x_range, dist.pdf(x_range))
	plt.savefig(os.path.join("test_output", "intercustomer_arrival_time_dist_{}.png".format(plot_name)))
	plt.clf()


@pytest.mark.parametrize("t, in_lunchtime", [
    (0, False),
    (2, False), # boundary case
    (3, True),
    (4, False), # boundary case
    (5, False),
])
def test_lunchtime(sim, t, in_lunchtime):
	sim.t = t
	assert sim.in_lunchtime() == in_lunchtime


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
def test_rush_period(sim, t, in_rush_period):
	sim.t = t
	assert sim.in_rush_period() == in_rush_period


@pytest.mark.parametrize("t, is_closing", [
    (0, False),
    (12, True), # boundary case
    (13, True),
])
def test_is_closing(sim, t, is_closing):
	sim.t = t
	assert sim.is_closing() == is_closing

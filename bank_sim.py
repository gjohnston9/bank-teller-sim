from scipy import stats

class BankSimulation():
	def __init__(self):
		### parameters (should be args)
		self.lunch_break_length = 0.75
		self.num_tellers = 2

		self.t = 0 # current time


	### Utility functions 

	def get_truncated_normal(self, mean, std_dev, low, high):
		a, b = (low - mean) / std_dev, (high - mean) / std_dev
		return stats.truncnorm(a, b, loc=mean, scale=std_dev)

	def in_rush_period(self):
		return (2 < self.t < 4) or (8 < self.t < 10)

	def in_lunchtime(self):
		return (2 < self.t < 4)


	### Probability distributions (defined in their own functions to make testing easier)

	def get_time_before_next_arrival_distribution(self):
		if (self.in_rush_period()):
			return self.get_truncated_normal(0.04, 0.04, 0, 0.08)
		else:
			return self.get_truncated_normal(0.08, 0.04, 0, 0.16)

	def get_transaction_time_distribution(self):
		return self.get_truncated_normal(0.2, 0.04, 0, 0.4)

	def get_lunch_break_distribution(self):
		return self.get_truncated_normal(3, 1, 2, 4)


	### Functions that use the distributions above to return an immediately useful value

	def get_rand_time_before_next_arrival(self):
		return get_time_before_next_arrival_distribution.rvs()

	def get_rand_customer_transaction_time(self):
		return self.get_transaction_time_distribution.rvs()

	def will_i_take_a_lunch_break(self):
		return (t > self.lunch_break_prob.rvs())

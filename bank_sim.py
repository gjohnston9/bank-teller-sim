from scipy import stats

import argparse
import time

from engine import Engine
from engine import Event
import evaluation

### Events specific to this simulation
###
### Each saves a reference to the simulation using it, so that we can access and
### update that simulation's methods and state variables
class Arrival(Event):
    ### Represents the arrival of a new customer
    def __init__(self, timestamp, sim):
        self.timestamp = timestamp
        self.sim = sim

    def callback(self):
        if not self.sim.is_closing(): # schedule the next arrival
            next_arrival_delay = self.sim.get_rand_time_before_next_arrival()
            next_arrival_time = self.sim.t + next_arrival_delay
            self.sim.engine.schedule(Arrival(next_arrival_time, self.sim))

        if (self.sim.num_waiting > 0) or (self.sim.num_idle == 0): # customer joins the line
            self.sim.num_waiting += 1
            self.sim.arrival_times.append(self.sim.t)
        else: # customer is immediately served
            self.sim.waiting_times.append(0) # no waiting for this customer
            self.sim.num_idle -= 1 # a teller becomes busy
            self.sim.num_busy += 1
            transaction_time = self.sim.get_rand_customer_transaction_time() # schedule the end of the transaction
            finished_time = self.sim.t + transaction_time
            self.sim.engine.schedule(FinishedService(finished_time, self.sim))


class FinishedService(Event):
    ### Represents the completion of a customer's interaction with a teller
    def __init__(self, timestamp, sim):
        self.timestamp = timestamp
        self.sim = sim

    def callback(self):
        self.sim.num_busy -= 1 # a teller becomes free
        self.sim.num_idle += 1

        if (self.sim.will_i_take_a_lunch_break()):
            if debug: print("teller {} is taking a lunch break, starting at time {} and lasting for {} hours".format(
                self.sim.num_lunch_breaks_taken, self.sim.t, self.sim.lunch_break_length))
            self.sim.num_lunch_breaks_taken += 1
            self.sim.num_idle -= 1 # the teller who just finished takes a lunch break
            self.sim.num_lunch += 1
            finished_time = self.sim.t + self.sim.lunch_break_length
            self.sim.engine.schedule(FinishedLunchBreak(finished_time, self.sim))
        else:
            self.sim.engine.schedule(TellerBecomesFree(self.sim.t, self.sim)) # teller calls next customer


class FinishedLunchBreak(Event):
    ### Represents the completion of a teller's lunchbreak
    def __init__(self, timestamp, sim):
        self.timestamp = timestamp
        self.sim = sim

    def callback(self):
        self.sim.num_lunch -= 1 # teller comes back from lunch
        self.sim.num_idle += 1
        self.sim.engine.schedule(TellerBecomesFree(self.sim.t, self.sim)) # teller calls next customer


class TellerBecomesFree(Event):
    ### Represents a teller who has just become idle, who will then call the next customer in line if there are any
    def __init__(self, timestamp, sim):
        self.timestamp = timestamp
        self.sim = sim

    def callback(self):
        if (self.sim.num_waiting > 0): # serve the customer who is first in line
            arrival_time = self.sim.arrival_times.pop(0)
            waiting_time = self.sim.t - arrival_time # determine how long this customer has been waiting for
            self.sim.waiting_times.append(waiting_time)
            self.sim.num_waiting -= 1

            self.sim.num_idle -= 1 # the teller becomes busy
            self.sim.num_busy += 1
            transaction_time = self.sim.get_rand_customer_transaction_time() # schedule the end of the transaction
            finished_time = self.sim.t + transaction_time
            self.sim.engine.schedule(FinishedService(finished_time, self.sim))


class BankSimulation():
    def __init__(self, lunch_break_length, num_tellers):
        self.engine = Engine()

        ### parameters
        self.lunch_break_length = lunch_break_length
        self.num_tellers = num_tellers

        ### state variables
        self.t = 0 # current time
        self.num_waiting = 0 # number of customers in line
        self.num_idle = self.num_tellers # all tellers start the day as idle
        self.num_busy = 0 # number of busy tellers
        self.num_lunch = 0 # number of tellers on lunch break
        self.num_lunch_breaks_taken = 0

        self.arrival_times = [] # used to calculate waiting time for each customer
        self.waiting_times = [] # returned after running simulation
        self.num_waiting_list = [] # also returned

    ### Utility functions 

    def get_truncated_normal(self, mean, std_dev, low, high):
        a, b = (low - mean) / std_dev, (high - mean) / std_dev
        return stats.truncnorm(a, b, loc=mean, scale=std_dev)

    def in_rush_period(self):
        return (2 < self.t < 4) or (8 < self.t < 10)

    def in_lunchtime(self):
        return (2 < self.t < 4)

    def is_closing(self):
        ### after 12 hours of operation, the bank stops accepting new customers in line
        return (self.t >= 12)

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
        return self.get_time_before_next_arrival_distribution().rvs()

    def get_rand_customer_transaction_time(self):
        return self.get_transaction_time_distribution().rvs()

    def will_i_take_a_lunch_break(self):
        return (self.num_lunch_breaks_taken < self.num_tellers) and \
            (self.t > self.get_lunch_break_distribution().rvs())


    def run_simulation(self):
        self.engine.schedule(Arrival(0, self))
        event = self.engine.remove()
        counter = 0
        while (event != None) and (counter < float("inf")):
            assert self.t <= event.timestamp
            if debug: print("t is {:4.2f}\tevent timestamp is {:4.2f}\tevent type is {:22}\tnum_waiting: {}".format(
                self.t, event.timestamp, event.__class__.__name__, self.num_waiting))
            self.num_waiting_list.append(self.num_waiting)
            self.t = event.timestamp
            event.callback()
            event = self.engine.remove()
            counter += 1
        print("finished simulation")
        return {
            "waiting_times" : self.waiting_times,
            "num_waiting_list" : self.num_waiting_list,
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("lunch_break_length", type=float, help="length of each teller's lunch break (in hours)")
    parser.add_argument("num_tellers", type=int, help="number of tellers at the bank")
    parser.add_argument("--verbose", action="store_true", help="provide additional simulation output")

    args = parser.parse_args()
    debug = args.verbose

    start_time = time.time()
    sim = BankSimulation(args.lunch_break_length, args.num_tellers)
    results = sim.run_simulation()
    end_time = time.time()

    print("took {:.2f} seconds to run".format(end_time - start_time))
    print(evaluation.get_statistics(results["waiting_times"]))

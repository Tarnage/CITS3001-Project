import unittest
import Agents
from InfoSimulator import *

class TestGreenAgents(unittest.TestCase):

    def setUp(self) -> None:
        self.broad_interval = [-0.5, 0.5]
        self.connect_prob_1 = [10, 0.4] # I think if I can remember probability! the probroablity of num_greens knowing each other is 50%
        self.grey_proportion_low = 0.1 # 10% chance grey is working for Red team
        self.sim = InfoSimulator(self.broad_interval, self.connect_prob_1[0], self.connect_prob_1[1], self.grey_proportion_low)

        self.blue = self.sim.blue_agent
        self.red = self.sim.red_agent
        self.green_network = self.sim.social_network


    def test_evaluate_state(self):
        self.sim.update_vote_status()
        points = self.sim.evaluateState(self.green_network, self.red, self.blue)
        print(f"Current Green Population Voting Status:")
        print(f"Will Vote: {self.sim.num_will_vote}")
        print(f"Not Vote: {self.sim.num_not_vote}")
        print(f"\nGAME START: {points}")

        return 

if __name__ == '__main__':
    unittest.main(verbosity=2)
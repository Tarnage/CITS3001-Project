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


        self.green_zero = Agents.Green_Agent(self.broad_interval, 0)
        self.green_one = Agents.Green_Agent(self.broad_interval, 1)


    def test_opinion_change(self):
        alpha = -0.6
        beta = 0.2
        result = self.sim.caculate_opinion_change(alpha, beta)
        self.assertAlmostEqual(result, -0.4)
        return 


    def test_red_influence_more_uncertain_no_change(self):
        alpha = -0.6
        red_voting = False
        beta = -0.3
        green_voting = True
        self.green_one.uncert = beta
        self.green_one.voting = green_voting
        
        result = self.sim.caculate_opinion_change(alpha, beta)
        self.assertAlmostEqual(result, -0.3)

        self.green_one.add_unert_values(result, red_voting)
        uncert = self.green_one.get_uncert_value()
        voting = self.green_one.get_vote_status()
        self.assertEqual(voting, green_voting, "Green is less sure of current vote but hasnt change its mind")
        self.assertAlmostEqual(uncert, -0.00, msg="Green becomes less uncertain about voting")

        #print(f'\nIs voting: {voting}: OPINION NOW: {uncert}')
        
    def test_red_influence_no_change(self):
        alpha = -0.6
        red_voting = False
        beta = -0.6
        green_voting = False
        self.green_one.uncert = beta
        self.green_one.voting = green_voting
        
        result = self.sim.caculate_opinion_change(alpha, beta)
        self.assertAlmostEqual(result, 0.0)


        self.green_one.add_unert_values(result, red_voting)
        uncert = self.green_one.get_uncert_value()
        voting = self.green_one.get_vote_status()
        self.assertEqual(voting, green_voting, "Green no change")
        self.assertAlmostEqual(uncert, -0.6, msg="Green no change")

    def test_red_influence_change_voting(self):

        alpha = -0.6
        red_voting = False
        beta = 0.3
        green_voting = True
        self.green_one.uncert = beta
        self.green_one.voting = green_voting
        
        result = self.sim.caculate_opinion_change(alpha, beta)
        self.assertAlmostEqual(result, -0.3)

        self.green_one.add_unert_values(result, red_voting)
        uncert = self.green_one.get_uncert_value()

        self.assertAlmostEqual(uncert, 0.0, msg="Failed to add the proper uncertainty")

        voting = self.green_one.get_vote_status()
        self.assertEqual(voting, green_voting, "Green no change")
        self.assertAlmostEqual(uncert, 0.0, msg="Green no change")




if __name__ == '__main__':
    unittest.main(verbosity=2)
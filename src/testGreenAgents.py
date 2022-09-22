import unittest
import Agents


class TestGreenAgents(unittest.TestCase):


    def setUp(self) -> None:
        self.agent = Agents.Green_Agent()


    def test_constructor(self):
        self.assertTrue(isinstance(self.agent, Agents.Green_Agent))

        expected = 0.0
        self.assertEqual(self.agent.get_will_vote(), expected, \
            msg=f"\nExpected: {expected}\nGot: {self.agent.will_vote} ")

        self.assertEqual(self.agent.get_not_vote(), expected, \
            msg=f"\nExpected: {expected}\nGot: {self.agent.not_vote} ")


    def test_set_will_vote(self):
        expected = 0.43
        self.agent.set_will_vote(expected)
        self.assertEqual(self.agent.get_will_vote(), expected, \
            msg=f"\nNormal Test\nExpected: {expected}\nGot: {self.agent.get_will_vote()} ")

        expected = 0.999
        self.agent.set_will_vote(expected)
        self.assertEqual(self.agent.get_will_vote(), expected, \
            msg=f"\nHigh Test\nExpected: {expected}\nGot: {self.agent.get_will_vote()} ")

        expected = -0.999
        self.agent.set_will_vote(expected)
        self.assertEqual(self.agent.get_will_vote(), expected, \
            msg=f"\nHigh Negative Test\nExpected: {expected}\nGot: {self.agent.get_will_vote()} ")

        expected = 0.00
        self.agent.set_will_vote(expected)
        self.assertEqual(self.agent.get_will_vote(), expected, \
            msg=f"\nZero Test\nExpected: {expected}\nGot: {self.agent.get_will_vote()} ")

        expected = 1.0
        self.agent.set_will_vote(expected)
        self.assertTrue(self.agent.get_will_vote() <= expected, \
            msg=f"\nMax Test\nExpected: {expected}\nGot: {self.agent.get_will_vote()} ")

        expected = -1.0
        self.agent.set_will_vote(expected)
        self.assertTrue(self.agent.get_will_vote() >= expected, \
            msg=f"\nMin Test\nExpected: {expected}\nGot: {self.agent.get_will_vote()} ")

        fail_test = 1.05
        expected = 1.0
        self.agent.set_will_vote(fail_test)
        self.assertTrue(self.agent.get_will_vote() <= expected, \
            msg=f"\nMax Test\nExpected: less than or equal to {expected}\nGot: {self.agent.get_will_vote()} ")

        fail_test = -1.34
        expected = -1.0
        self.agent.set_will_vote(fail_test)
        self.assertTrue(self.agent.get_will_vote() >= expected, \
            msg=f"\nMax Test\nExpected: less than or equal to {expected}\nGot: {self.agent.get_will_vote()} ")


    def test_set_not_vote(self):
        expected = 0.43
        self.agent.set_not_vote(expected)
        self.assertEqual(self.agent.get_not_vote(), expected, \
            msg=f"\nNormal Test\nExpected: {expected}\nGot: {self.agent.get_not_vote()} ")

        expected = 0.999
        self.agent.set_not_vote(expected)
        self.assertEqual(self.agent.get_not_vote(), expected, \
            msg=f"\nHigh Test\nExpected: {expected}\nGot: {self.agent.get_not_vote()} ")

        expected = -0.999
        self.agent.set_not_vote(expected)
        self.assertEqual(self.agent.get_not_vote(), expected, \
            msg=f"\nHigh Negative Test\nExpected: {expected}\nGot: {self.agent.get_not_vote()} ")

        expected = 0.00
        self.agent.set_not_vote(expected)
        self.assertEqual(self.agent.get_not_vote(), expected, \
            msg=f"\nZero Test\nExpected: {expected}\nGot: {self.agent.get_not_vote()} ")

        expected = 1.0
        self.agent.set_not_vote(expected)
        self.assertTrue(self.agent.get_not_vote() <= expected, \
            msg=f"\nMax Test\nExpected: {expected}\nGot: {self.agent.get_not_vote()} ")

        expected = -1.0
        self.agent.set_not_vote(expected)
        self.assertTrue(self.agent.get_not_vote() >= expected, \
            msg=f"\nMin Test\nExpected: {expected}\nGot: {self.agent.get_not_vote()} ")

        fail_test = 1.05
        expected = 1.0
        self.agent.set_not_vote(fail_test)
        self.assertTrue(self.agent.get_not_vote() <= expected, \
            msg=f"\nMax Test\nExpected: less than or equal to {expected}\nGot: {self.agent.get_not_vote()} ")

        fail_test = -1.34
        expected = -1.0
        self.agent.set_not_vote(fail_test)
        self.assertTrue(self.agent.get_not_vote() >= expected, \
            msg=f"\nMax Test\nExpected: less than or equal to {expected}\nGot: {self.agent.get_not_vote()} ")


    def test_get_rand(self):
        got = self.agent.get_rand()
        self.assertTrue(got >= 0, \
            msg=f"\nProbability number test\nExpected: number greater than equal to 0.0\nGot: {got}")
        
        got = self.agent.get_rand()
        self.assertTrue(got <= 1.0, \
            msg=f"\nProbability number test\nExpected: number less than equal to 1.0\nGot: {got}")


    def test_get_connections(self):
        adjlist = self.agent.get_connections()
        expected = 0
        self.assertEqual(len(adjlist), expected, \
            msg=f"\nChecking adjency list\nExpected: {expected}\nGot: {len(adjlist)}")

        self.agent.add_connection(2)
        expected = 1
        self.assertEqual(len(adjlist), expected, \
            msg=f"\nChecking adjency list\nExpected: {expected}\nGot: {len(adjlist)}")

        self.assertEqual(adjlist[0], 2, \
            msg=f"\nChecking adjency list\nExpected: {2}\nGot: {adjlist[0]}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
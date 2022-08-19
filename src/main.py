import Agents
import numpy

class Info_Simulator:
    def __init__(self, num_green: int, uncert_ints: list, connect_prob: list, grey_proportion: int) -> None:
        self.green_agent_adjlist = self.create_green_agents(num_green, uncert_ints, connect_prob)
        self.red_agent = Agents.Red_Agent()
        self.blue_agent = Agents.Blue_Agent()
        self.grey_agent = Agents.Grey_Agent(grey_proportion)

    
    def create_green_agents(num_green: int, uncert_ints: list, connect_prob: list) -> list:
        # TODO:
        # Init num_green agents
        # Apply uncert_ints to will_vote and not_vote
        # Use connect_prob to create the adjlist of green agents connections with each other

        return


    def run():

        finished = False
        while not finished:
            break



if __name__ == "__main__":

    # Example of current acceptable inputs
    # May change as we learn more and program evolves
    num_green = 10
    broad_interval = [-0.5, 0.5]
    tight_interval = [-0.9, 0.1]
    connect_prob = [num_green, 0.5] # I think if I can remember probability! the probroablity of num_greens knowing each other is 50%
    connect_prob = [num_green, 0.1] # num_greens knowing each other is 10%, again might need to confirm n and p values
    grey_proportion_high = 0.8 # 80% chance grey is working for Red team
    grey_proportion_low = 0.1 # 10% chance grey is working for Red team

    sim = Info_Simulator(num_green, broad_interval, connect_prob, grey_proportion_high)
    sim.run()
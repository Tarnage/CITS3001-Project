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
        # Use connect_prob to create the adjlist of green agents connections
        
        return


    def run():

        finished = False
        while not finished:
            break



if __name__ == "__main__":
    sim = Info_Simulator()
    sim.run()
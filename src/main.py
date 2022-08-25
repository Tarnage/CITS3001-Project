import Agents
import numpy

class InfoSimulator:
    def __init__(self, num_green: int, uncert_ints: list, connect_prob: list, grey_proportion: int) -> None:
        self.red_agent = Agents.Red_Agent()
        self.blue_agent = Agents.Blue_Agent()
        self.grey_agent = Agents.Grey_Agent(grey_proportion)
        self.green_list = list()

        self.create_green_agents(num_green, connect_prob)
    

    def create_green_agents(self, num_green: int, connect_prob: list) -> None:
        n = connect_prob[0]
        p = connect_prob[1]
        x = (n*p) / 100
        
        # construct num_green of Green Agents
        for i in range(num_green):
            new_agent = Agents.Green_Agent(connect_prob)
            self.green_list.append(new_agent)

        # Check for connections between green agents
        for i, agent in enumerate(self.green_list):

            for j in range(i+1, num_green):

                # When is j less than i we have already checked those connections
                # Thats why we start at  i+1
                
                agent_1_prob = agent.get_prob_value()
                agent_2_prob = self.green_list[j].get_prob_value()
                
                # check if agent has a connection
                if (agent_1_prob < x) and (agent_2_prob < x):
                    agent.add_connection(j)
                    self.green_list[j].add_connection(i)


    def run():

        finished = False
        while not finished:
            break

    
    def print_green_adjlist(self):
        for i, agent in enumerate(self.green_list):
            adj_list = agent.get_connections()
            print(f"Agent #{i}: ", end="")
            for j in adj_list:
                print(f'{j} ', end="")
            print()


if __name__ == "__main__":

    # Example of current acceptable inputs
    # May change as we learn more and program evolves
    num_green = 10
    percent_will_vote = 0.5
    broad_interval = [-0.5, 0.5]
    tight_interval = [-0.9, 0.1]
    connect_prob = [40, 0.5] # I think if I can remember probability! the probroablity of num_greens knowing each other is 50%
    connect_prob = [50, 0.1] # num_greens knowing each other is 10%, again might need to confirm n and p values
    grey_proportion_high = 0.8 # 80% chance grey is working for Red team
    grey_proportion_low = 0.1 # 10% chance grey is working for Red team

    sim = InfoSimulator(num_green, broad_interval, connect_prob, grey_proportion_high)
    sim.run()
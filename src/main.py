import Agents
import numpy
import random as rand
import networkx as nx
import matplotlib.pyplot as plt

class InfoSimulator:
    def __init__(self, uncert_ints: list, n: int, p: int, grey_proportion: int) -> None:
        self.red_agent = Agents.Red_Agent()
        self.blue_agent = Agents.Blue_Agent()
        self.grey_agent = Agents.Grey_Agent(grey_proportion)
        self.green_list = list()
        self.n = n
        self.p = p
                
        # Create a graph for modelling
        self.g = nx.Graph()
        self.g.add_nodes_from(range(0, self.n))

        self.create_green_agents(self.n, self.p)


    

    def create_green_agents(self, n: int, p: list) -> None:
        
        # construct num_green of Green Agents
        for i in range(n):
            new_agent = Agents.Green_Agent()
            self.green_list.append(new_agent)

        # Check for connections between green agents
        for i, agent in enumerate(self.green_list):

            for j in range(i+1, n):

                # When is j less than i we have already checked those connections
                # Thats why we start at  i+1
                
                agent_1_prob = agent.get_prob_value()
                agent_2_prob = self.green_list[j].get_prob_value()
                
                # check if agent has a connection
                # we can just compare one agent instead of two.
                # We should simulate what happens
                if (agent_1_prob < p) and (agent_2_prob < p):

                    # add to g for modelling
                    self.g.add_edge(i, j)

                    # add to agents adjlist
                    agent.add_connection(j)
                    self.green_list[j].add_connection(i)


    def run(self):

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


    def print_distrubution_graph(self, display="graph"):
            # Print the number of connections a green agent has
            print(nx.degree(self.g))

            if display == "graph":
                # print the current green network
                pos = nx.circular_layout(self.g)
                nx.draw(self.g, pos, with_labels=1)
                plt.show()

            if display == "distribution":
                # This plot should resemble a bionomoial distribution

                all_degrees = list(dict((nx.degree(self.g))).values())
                unique_degrees = list(set(all_degrees))
                unique_degrees.sort()
                nodes_with_degrees = list()

                for i in unique_degrees:
                    nodes_with_degrees.append(all_degrees.count(i))
                
                plt.plot(unique_degrees, nodes_with_degrees)
                plt.xlabel("Connections")
                plt.ylabel("No. of Green Agents")
                plt.title("Green Agent Connection Distribution")
                plt.show()
            

if __name__ == "__main__":

    # Example of current acceptable inputs
    # May change as we learn more and program evolves
    num_green = 10
    percent_will_vote = 0.5
    broad_interval = [-0.5, 0.5]
    tight_interval = [-0.9, 0.1]
    connect_prob_1 = [20, 0.4] # I think if I can remember probability! the probroablity of num_greens knowing each other is 50%
    connect_prob_2 = [50, 0.1] # num_greens knowing each other is 10%, again might need to confirm n and p values
    grey_proportion_high = 0.8 # 80% chance grey is working for Red team
    grey_proportion_low = 0.1 # 10% chance grey is working for Red team

    sim = InfoSimulator(broad_interval, connect_prob_1[0], connect_prob_1[1], grey_proportion_high)
    sim.run()
    #sim.print_distrubution_graph(display="distribution")
    #sim.print_distrubution_graph(display="graph")

    sim.print_green_adjlist()
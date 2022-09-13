import Agents
import numpy
import random as rand
import networkx as nx
import matplotlib.pyplot as plt
import Metrics


class InfoSimulator:
    def __init__(self, uncert_ints: list, n: int, p: int, grey_proportion: int) -> None:
        self.social_network = list()
        self.red_agent = Agents.Red_Agent()
        self.blue_agent = Agents.Blue_Agent()
        self.grey_agent = Agents.Grey_Agent(grey_proportion)
        self.metrics = Metrics.Metrics()
        self.n = n
        self.p = p

        self.social_network.append(self.red_agent)
        self.social_network.append(self.blue_agent)
        self.social_network.append(self.grey_agent)

        # Create a graph for modelling
        self.model = nx.Graph()
        self.create_green_agents(self.n, self.p)

    def create_green_agents(self, n: int, p: list) -> None:

        # construct num_green of Green Agents
        for i in range(n):
            new_agent = Agents.Green_Agent()
            self.social_network.append(new_agent)
            #adding red agent to connect to all
            self.red_agent.connections.append(new_agent)
            #connecting the red to everything


        # Check for connections between green agents
        for i, agent in enumerate(self.social_network):

            for j in range(i+1, n):

                # When is j less than i we have already checked those connections
                # Thats why we start at  i+1

                    team_one = agent.get_team()
                    team_two = self.social_network[j].get_team()

                    if not (team_one == "green") and \
                       (team_two == "green"):

                        agent_1_prob = agent.get_prob_value()
                        agent_2_prob = self.social_network[j].get_prob_value()
                        
                        # check if agent has a connection
                        # we can just compare one agent instead of two.
                        # We should simulate what happens
                        if (agent_1_prob < p) and (agent_2_prob < p):

                            # add to g for modelling
                            self.model.add_edge(i, j)

                            # add to agents adjlist
                            agent.add_connection(j)
                            self.social_network[j].add_connection(i)


    def run(self):
        while self.blue_agent.get_energy() > 0 :
            self.Red_Turn()
            self.metrics.display_network(self.model, display="graph")
            self.Blue_Turn()
            self.metrics.display_network(self.model, display="graph")
            self.Green_Turn()
            self.metrics.display_network(self.model, display="graph")



    #ill make a game class for this
    def Red_Turn(self):
        # give 5 options 
        opinionGain = [10,15,20,25,30]
        followerLost = [0,5,10,15,20] # percentage
        print(opinionGain)
        print(followerLost)
        option = int(input("Choose Options 1-5: ") )- 1 
        
        # Lose Followers
        self.Lose_Followers(followerLost[option])

        # Change remaining green opinion
        self.Change_Opinion(opinionGain[option], False)
        return


    def Blue_Turn(self):

        # give 5 options
        opinionGain = [10,15,20,25,30]
        energyLost = [0,5,10,15,20]
        print(opinionGain)
        print(energyLost)
        print("current blue energy = " + str(self.blue_agent.get_energy()) + "\n")
        option = int(input("Choose Options 1-5: ") )- 1 
        # Change green opinion
        self.Change_Opinion(opinionGain[option], True)

        # Lose Energy
        self.blue_agent.lose_energy(energyLost[option])
        
        #Have option for adding Grey
        return

    def Green_Turn(self):
        #set their current side
        opinionChange = 5 
        for agent in self.social_network:
            agent.current_side()
            #Mingle with eachother and effect opinions
            for connection in agent.connections:
                if agent.get_side():
                    self.social_network[connection].add_vote(opinionChange)
                else:
                   self.social_network[connection].add_not_vote(opinionChange)

        # Adding a grey will give it an opinion 
        return


    def Lose_Followers( self , percentage: int):
        numA = len(self.red_agent.connections) - 1
        for i in range(int(numA*percentage/100)):
            #just removing random agents for now
            node = rand.randrange(numA)
            self.red_agent.remove_connections(node)
        return

    def Change_Opinion(self, amount: int, voting: bool):

        if voting: # affecting everyone for now 
            for agent in self.social_network:
                if  not isinstance(agent, Agents.Blue_Agent) and \
                    not isinstance(agent, Agents.Red_Agent) and \
                    not isinstance(agent, Agents.Grey_Agent):
                        agent.add_vote(amount)
        else:  
            for agent in self.red_agent.connections:
                agent.add_not_vote(amount)
        return



    def add_connections(self):

        for i, agent in enumerate(self.green_list):
            conn_list = agent.get_connections()
            for conn in conn_list:
                self.g.add_edge(i, conn)


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

    #sim.print_green_adjlist()
from turtle import color
import Agents
import numpy
import random as rand
import networkx as nx
import matplotlib.pyplot as plt
1
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
        
        self.create_green_agents(self.n, self.p)
        
        


    

    def create_green_agents(self, n: int, p: list) -> None:
        
        self.green_list = list()

        # construct num_green of Green Agents
        for i in range(n):
            new_agent = Agents.Green_Agent()
            self.green_list.append(new_agent)
            #adding red agent to connect to all
            self.red_agent.connections.append(new_agent)
            #connecting the red to everything


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
        while self.blue_agent.get_energy() > 0 :
            self.Red_Turn()
            self.print_distrubution_graph(display="graph")
            self.Blue_Turn()
            self.print_distrubution_graph(display="graph")
            self.Green_Turn()
            self.print_distrubution_graph(display="graph")



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

        self.create_green_agents(self.n, self.p)

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
        for agent in self.green_list:
            agent.current_side()
            #Mingle with eachother and effect opinions
            for connection in agent.connections:
                if agent.get_side():
                    self.green_list[connection].add_vote(opinionChange)
                else:
                   self.green_list[connection].add_not_vote(opinionChange)

        # Adding a grey will give it an opinion 
        return


    def Lose_Followers( self , percentage: int):
        numA = len(self.red_agent.connections)
        for i in range(int(numA*percentage/100)):
            #just removing random agents for now
            node = rand.randrange(numA)
            self.red_agent.remove_connections(node)
        return

    def Change_Opinion(self, amount: int, voting: bool):
        if voting: # affecting everyone for now 
            for agent in self.green_list:
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



    def print_green_adjlist(self):
        for i, agent in enumerate(self.green_list):
            adj_list = agent.get_connections()
            print(f"Agent #{i}: ", end="")
            for j in adj_list:
                print(f'{j} ', end="")
            print()


    def print_distrubution_graph(self, display="graph"):
            self.g = nx.Graph()
            self.g.add_nodes_from(range(0, self.n))
            self.add_connections()
            # Print the number of connections a green agent has
            print(nx.degree(self.g))

            if display == "graph":
                # print the current green network
                pos = nx.circular_layout(self.g)

                plt.clf()
                nx.draw(self.g, pos, with_labels=1)
                plt.show(block=False)
                plt.pause(0.01)
                

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

    #sim.print_green_adjlist()
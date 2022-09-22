import Agents
import numpy
import random as rand
import networkx as nx
import Metrics


class InfoSimulator:
    def __init__(self, uncert_ints: list, n: int, p: int, grey_proportion: int) -> None:
        self.social_network = list()
        self.red_agent = Agents.Red_Agent()
        self.blue_agent = Agents.Blue_Agent()
        self.grey_agent = Agents.Grey_Agent(grey_proportion)
        self.metrics = Metrics.Metrics()
        self.current_turn = ""
        self.num_turns = 0

        self.num_will_vote = 0
        self.num_not_vote = 0

        # Create a graph for modelling
        self.model = nx.Graph()
        self.create_green_agents(uncert_ints, n, p)

    def create_green_agents(self, uncernt_ints, n: int, p: list) -> None:

        # construct num_green of Green Agents
        for i in range(n):
            new_agent = Agents.Green_Agent(uncernt_ints, i)
            self.social_network.append(new_agent)

            #----------------------Testing uncert values----------------
            print(f"Agent Social Security Number (ssn): {i}")
            print(f"Will vote: {new_agent.get_will_vote()}")
            print(f"Not vote: {new_agent.get_not_vote()}")
            #--------------------------------------------------------------

            # IF GREEN IS NOT VOTING IT IS A FOLLOWER OF RED
            if new_agent.get_vote_status() == False:
                self.red_agent.connections.append(i)

            # BLUE HAS A CONNECTION TO EVERYONE
            self.blue_agent.connections.append(i)

        # Check for connections between green agents
        for i, agent in enumerate(self.social_network):

            for j in range(i+1, n):

                # When is j less than i we have already checked those connections
                # Thats why we start at  i+1

                        agent_1_prob = agent.get_rand()
                        agent_2_prob = self.social_network[j].get_rand()
                        
                        # check if agent has a connection
                        # we can just compare one agent instead of two.
                        # We should simulate what happens
                        if (agent_1_prob < p) and (agent_2_prob < p):

                            # add to g for modelling
                            self.model.add_edge(i, j)

                            # add to agents adjlist
                            agent.add_connection(j)
                            self.social_network[j].add_connection(i)
        
        self.update_vote_status()


    def update_vote_status(self):
        for agent in self.social_network:
            if agent.get_vote_status() == True:
                self.num_will_vote += 1
            else:
                self.num_not_vote += 1


    def print_vote_status(self):
        print(f"Current Green Population Voting Status:")
        print(f"Will Vote: {self.num_will_vote}")
        print(f"Not Vote: {self.num_not_vote}")


    def choose_first_move(self):
        # TODO: allow human players to choose 0 (heads) or 1(tails) 
        if rand.randint(0, 1) == 0:
            self.current_turn = "blue"
        else:
            self.current_turn = "red"


    def get_current_turn(self):
        return self.current_turn


    def get_num_turns(self):
        return self.num_turns


    def increment_turns(self):
        self.num_turns += 1


    def run(self):
        try:
            # Randomly choose who goes first
            self.choose_first_move()

            while self.blue_agent.get_energy() > 0 :
                self.update_vote_status()
                self.print_vote_status()
                self.metrics.display_connections(self.red_agent, self.blue_agent, self.social_network)
                if self.get_current_turn() == "red":
                    self.red_turn()
                else:
                    self.blue_turn()
                
                self.increment_turns()
                # Greens turn after red and player have had their turns
                if self.get_num_turns() % 2 == 0:
                    self.green_turn()
                    # TODO: add grey turn
        except KeyboardInterrupt:
            print("Ending game...")

    def user_input(self):
        while True:
            option = input("Choose Options 1-5: ")
            try:
                val = int(option)
                if val > 4:
                    raise ValueError
                break
            except ValueError:
                print("This is not a number. Please enter a valid number")

        return int(option)-1


    #ill make a game class for this
    def red_turn(self):
        # give 5 options 
        opinionGain = [10,15,20,25,30]
        followerLost = [0,5,10,15,20] # percentage
        print(opinionGain)
        print(followerLost)
        
        option = self.user_input()

        # Lose Followers
        self.lose_followers(followerLost[option])

        # Change remaining green opinion
        self.change_opinion(opinionGain[option], False)
        return


    def blue_turn(self):

        # give 5 options
        opinionGain = [10,15,20,25,30]
        energyLost = [0,5,10,15,20]
        print(opinionGain)
        print(energyLost)
        print("current blue energy = " + str(self.blue_agent.get_energy()) + "\n")
        option = self.user_input()

        # Change green opinion
        self.change_opinion(opinionGain[option], True)

        # Lose Energy
        self.blue_agent.lose_energy(energyLost[option])
        
        #Have option for adding Grey
        return

    def green_turn(self):
        #set their current side
        opinionChange = 5 
        for agent in self.social_network:
            agent.set_voting()
            #Mingle with eachother and effect opinions
            for connection in agent.connections:
                if agent.get_voting_status():
                    self.social_network[connection].add_vote(opinionChange)
                else:
                   self.social_network[connection].add_not_vote(opinionChange)

        # Adding a grey will give it an opinion 
        return


    def lose_followers( self , percentage: int):
        numA = len(self.red_agent.connections)

        for i in range(int(numA*percentage/100)):
            #just removing random agents for now
            node = rand.randrange(numA)

            if node in self.red_agent.get_connections():
                self.red_agent.remove_connections(node)
        return

    def change_opinion(self, amount: int, voting: bool):
        if voting: # affecting everyone for now 
            for i, agent in enumerate(self.social_network):
                        self.social_network[i].add_not_vote(amount)
        else:  
            for i, agent in enumerate(self.social_network):
                self.social_network[i].add_not_vote(amount)
        return

    def add_connections(self):
        for i, agent in enumerate(self.social_network):
            conn_list = agent.get_connections()
            for conn in conn_list:
                self.g.add_edge(i, conn)


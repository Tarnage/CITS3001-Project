from json.encoder import INFINITY
import Agents
import numpy
import random as rand
import networkx as nx
import Metrics
import time
import copy
import logging
from datetime import datetime

BLUE_OPTIONS = {
    "DEPLOY_GREY": 6,
}

format = '%(message)s'
folder = f"./logs/"
logs = folder + datetime.now().strftime("%m.%d.%Y.%H.%M.%S")+'.log'


logging.basicConfig(level=logging.INFO, filename=logs, format=format)

'''
You can quit the game at any time by typing "quit" into the terminal
'''

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

        logging.info(f"Game Start:")
        logging.info(f"\tParameters: ")
        logging.info(f"\t\t Uncertainty Intervals: [{uncert_ints[0]}, {uncert_ints[1]}]")
        logging.info(f"\t\t Connection Probability: [{n}, {p}]")
        logging.info(f"\t\t Grey Proportions: {grey_proportion}")

    def create_green_agents(self, uncernt_ints, n: int, p: list) -> None:

        # construct num_green of Green Agents
        for i in range(n):
            new_agent = Agents.Green_Agent(uncernt_ints, i)
            self.social_network.append(new_agent)

            # IF GREEN IS NOT VOTING IT IS A FOLLOWER OF RED
            if new_agent.get_vote_status() == False:
                self.red_agent.connections.append(i)
                self.red_agent.increment_followers() #increment followers

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
        will_vote = 0
        not_vote = 0

        for agent in self.social_network:
            if agent.get_vote_status() == True:
                will_vote += 1
            else:
                not_vote += 1

        self.num_will_vote = will_vote
        self.num_not_vote = not_vote


    def print_vote_status(self):
        print(f"Current Green Population Voting Status:")
        print(f"Will Vote: {self.num_will_vote}")
        print(f"Not Vote: {self.num_not_vote}")
        logging.info(f"\t\tWill Vote: {self.num_will_vote}")
        logging.info(f"\t\tNot Vote: {self.num_not_vote}\n")


    def choose_first_move(self):
        # TODO: allow human players to choose 0 (heads) or 1(tails) 
        if rand.randint(0, 1) == 0:
            self.current_turn = "blue"
        else:
            self.current_turn = "red"


    def get_current_turn(self):
        return self.current_turn

    def set_current_turn(self, turn):
        self.current_turn = turn

    def get_num_turns(self):
        return self.num_turns

    def increment_turns(self):
        self.num_turns += 1

    def run(self):
        try:
            # Randomly choose who goes first
            self.choose_first_move()

            logging.info(f"Turn: {self.num_turns}")
            logging.info(f"\tWill Vote: {self.num_will_vote}")
            logging.info(f"\tNot Vote: {self.num_will_vote}")

            while self.blue_agent.get_energy() > 0 :
                # Updates and prints gloabl values before each turn
                self.metrics.display_connections(self.red_agent, self.blue_agent, self.social_network)
                time.sleep(2)
                if self.get_current_turn() == "red":
                    logging.info("\tRed Agents Turn:")
                    print("Red Agents Turn...")
                    self.red_turn()
                    time.sleep(2)
                    self.set_current_turn("blue")
                    self.update_vote_status()
                    self.print_vote_status()
                else:
                    logging.info("\tBlue Agents Turn:")
                    print("Blue Agents Turn...")
                    print(f"Current Energy: {self.blue_agent.get_energy()}")
                    self.blue_turn()
                    time.sleep(2)
                    self.set_current_turn("red")
                    self.update_vote_status()
                    self.print_vote_status()
                
                self.increment_turns()
                # Greens turn after red and blue have had their turns
                if self.get_num_turns() % 2 == 0:
                    logging.info("\tGreen Agents are interacting...")
                    print("Green Agents are interacting....")
                    time.sleep(2)
                    self.green_turn()
                    self.update_vote_status()
                    self.print_vote_status()

                    if self.grey_agent.is_active():
                        logging.info("\tThe Grey Agent is making its move:")
                        print("The Grey Agent is making its move....")
                        time.sleep(2)
                        self.grey_turn()
                        self.update_vote_status()
                        self.print_vote_status()

                    logging.info(f"Turn: {self.num_turns // 2}")

            self.check_winner()
        
        except KeyboardInterrupt:
            print("Ending game...")


    def check_winner(self):
        self.update_vote_status()
        self.print_vote_status()

        if self.num_will_vote > self.num_not_vote:
            print("BLUE AGENT WINS!!")
        elif self.num_will_vote < self.num_not_vote:
            print("RED AGENT WINS!!")
        else:
            print("ITS A TIE!")


    def user_input(self, team: str):
        while True:
            option = input("Choose Options: ")
            try:
                if option.isdigit():
                    if int(option) > 6:
                        raise ValueError
                    if int(option) == 6 and team == 'blue' and self.grey_agent.is_active():
                        print("Grey Agetn has already been deployed")
                elif option == "quit":
                    raise Exception
                break
            except ValueError:
                print("This is not a number. Please enter a valid number or type 'quit' to close the game")
            except Exception:
                print("Gracefully quiting game")
                exit(0)

        return int(option)


    def red_turn(self):
        # give 5 options 
        # print(opinionGain)
        # print(followerLost)
        
        #option = self.user_input("red")
        option = self.minimaxRed(self.social_network, self.blue_agent, self.red_agent, 1, True)[0]
        print("Choosing option :" + str(option))
        # Lose Followers
        lost = self.red_agent.followers_lost(option)
        self.lose_followers(lost)

        # Change remaining green opinion
        amount = self.red_agent.broadcast(option)
        self.change_opinion(amount , False)

        logging.info(f"\t\tUsing Option: {option}")
        logging.info(f"\t\tuncertainty: {self.red_agent.broadcast_options[option]}")
        logging.info(f"\t\tfollowers lost: {self.red_agent.broadcast_options[option]}")
        return


    def blue_turn(self):
        print("current blue energy = " + str(self.blue_agent.get_energy()) + "\n")
        self.blue_agent.print_moves()
        option = self.user_input("blue")

        logging.info(f"\t\tUsing Option: {option}")

        if option == BLUE_OPTIONS["DEPLOY_GREY"]:
            self.deploy_grey_agent()
            self.blue_agent.set_used_grey()
            logging.info(f"\t\tDeployed Grey Agent: ({self.grey_agent.get_team_alignment()})")
        else:
            opinion_gain = -(self.blue_agent.get_opinion_gain(option))
            logging.info(f"\t\tUncertainty Value: {opinion_gain}")
            logging.info(f"\t\tCurrent Energy: {opinion_gain}")
            # Change green opinion
            self.change_opinion(opinion_gain, True)
            # Lose Energy
            energy_lost = self.blue_agent.lose_energy(option)
            logging.info(f"\t\tEnergy Lost: {energy_lost}")
            


    def deploy_grey_agent(self):
        self.grey_agent.set_active()


    def grey_turn(self):
        # Grey has a connection to everyone
        uncert_values = self.grey_agent.uncert
        is_voting = False

        if self.grey_agent.get_team_alignment() == "blue":
            is_voting = True
        else:
            is_voting = False

        self.change_opinion(uncert_values, is_voting)


    def green_turn(self):
        #set their current side
        for agent in self.social_network:
            # Mingle with eachother and effect opinions
            is_voting = agent.get_vote_status()
            curr_agent_uncert = agent.get_uncert_value()
            for connection in agent.connections:
                green_two = self.social_network[connection]
                # if agent is voting it will try to convince others to vote else if will try to convince
                # changing the agents opinion
                green_two_uncert = green_two.get_uncert_value()
                opinion_change = self.caculate_opinion_change(curr_agent_uncert, green_two_uncert)
                green_two.add_unert_values(opinion_change, is_voting)


    def caculate_opinion_change(self, alpha: float, beta: float) -> float:
        '''
            Formula: 
                f(n) = 
                    (alpha + beta) if beta < 0.0
                    (alpha - beta) if beta >= 0.0
                    
            Params:
                alpha: float the uncertainty of the influencer
                beta: float the uncertainty of the agent being influenced
            
            Return:
                result: float value of how much alpha can influence beta
        '''

        if beta < 0.00:
            return round(alpha - beta, 2)
        else:
            return round(alpha + beta, 2)


    def lose_followers( self , percentage: int):
        numA = len(self.red_agent.connections)

        for i in range(int(numA*percentage/100)):
            #just removing random agents for now
            node = rand.randrange(numA)

            if node in self.red_agent.get_connections():
                self.red_agent.remove_connections(node)
                self.red_agent.decrement_followers()
                print("RED LOST A FOLLOWER")
        return


    def change_opinion(self, amount: float, is_voting: bool):
        '''
            This change opinion is used for blue, and grey agents as they can talk to everyone

        '''
        for agent in self.social_network:
            prev_voting = agent.get_vote_status()
            agent.add_unert_values(amount, is_voting)
            new_voting = agent.get_vote_status()

            if not prev_voting == new_voting:
                print("Opinion Changed")
        return



    # Use this for the minimax it will return the number of greens that have chnaged their opinion
    def simulate_change_opinion(self, deep_copy, amount: int, is_voting: bool):
        num_opinion_change = 0
        for agent in deep_copy:
            prev_voting = agent.get_vote_status()
            agent.add_unert_values(amount, is_voting)
            new_voting = agent.get_vote_status()

            if not prev_voting == new_voting:
                num_opinion_change += 1
        #dont need return yet
        return num_opinion_change

    def simulate_red_lost(self, red, option):
        #will need to do a deepcopy agent and so that different routes could be taken.
        # will use AVERAGE amounts (possibly take into consideration, min and max interval if we change it from a flat amount. )
        red.followers_lost(option, average = True) 
        return red.broadcast(option, average = True) 
        

    def simulate_blue_energy(self, blueAgent, option):
        blueAgent.lose_energy(option, average = True)
        return blueAgent.get_opinion_gain(option, average = True)

    def simulate_green_turn(self):
        pass

    def add_connections(self):
        for i, agent in enumerate(self.social_network):
            conn_list = agent.get_connections()
            for conn in conn_list:
                self.g.add_edge(i, conn)

    def minimaxRed(self, green, blue, red, depth: int, Maxteam: bool): 
        #maxteam false - blues turn
        #thinking of having it in this file so both teams can call it and both teams can have a view of the current green population EDIT: just doing red first
        #need a heuristic function
        #Gamestate needs to be updated to be sent to the Minimax, should present copy of social network
        if self.isterminal(blue): #blue team is dead  checking gamestate, basically the only terminal node is if the blue is dead. 
            if self.RedWinning(green):
                return (-1, 100000000)
            else:
                return (-1,-100000000)
        elif depth == (0):
            return (-1,self.evaluateState(green, red, blue))


        if Maxteam:
            value = -INFINITY
            choice =  rand.randint(0,6)
            for option in range(len(self.red_agent.broadcast_options)): 
                print(option)
                green_Copy = copy.deepcopy(self.social_network)
                red_Copy = copy.deepcopy(self.red_agent)        
                opinion_change = self.simulate_red_lost(red_Copy, option)
                self.simulate_change_opinion(green_Copy, opinion_change, False)
                new_score = self.minimaxRed(green_Copy, blue, red_Copy, depth-1, 0)

                if new_score[1] > value:
                    value = new_score[1]
                    if new_score[0] == -1:
                        choice = option
                    else:
                        choice = new_score[0]
            return (choice, value)
        
        else:
            value = INFINITY
            choice =  rand.randint(0,6)
            for option in range(len(self.blue_agent.opinion_gain)): 
                green_Copy = copy.deepcopy(self.social_network)
                blue_Copy = copy.deepcopy(self.blue_agent)
                opinion_change = self.simulate_blue_energy(blue_Copy, option)
                self.simulate_change_opinion(green_Copy, opinion_change, True)
                new_score = self.minimaxRed(green_Copy, blue_Copy, red, depth -1, 1)

                if new_score[1] < value:
                    value = new_score[1]
                    if new_score[0] == None:
                        choice = option
                    else:
                        choice = new_score[0]
            return (choice, value)
        

    def isterminal(self, blue):
        if blue.get_energy() == 0: #need to also check if they have a grey agent left still
            return True
        return False
        #check if blue is dead. 

    def RedWinning(self, network):
        redFollowers = 0
        blueFollowers = 0
        for agent in network:
            if agent.get_vote_status():
                blueFollowers += 1
            else:
                redFollowers += 1
        return redFollowers > blueFollowers #winning move

    def evaluateState(self, greenNetwork, red, blue):
        #evaluate who is currently winning and return a point value 
        points = 0
        for agent in greenNetwork:
            if agent.get_vote_status():
                points -= 5
            else: 
                points += 5
        
        points += int((100-blue.get_energy())/10) #less energy, better for red?

        points += red.get_followers()

        return points

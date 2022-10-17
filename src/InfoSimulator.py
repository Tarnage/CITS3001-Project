import Agents
import numpy
import random as rand
import networkx as nx
import Metrics
import time
import copy
import logging
from datetime import datetime
import math
import os
import sys

def check_dir(peer_dir: str):
    ''' Helper to make sure temp directory exists if not create one
        Args;
            peer_dir(str): name of the directory to check
    '''
    if not os.path.isdir(peer_dir):
        try:
            os.mkdir(peer_dir)
        except OSError as err:
            sys.exit("Directory creation failed with error: {err}")

BLUE_OPTIONS = {
    "DEPLOY_GREY": 6,
}

# Check logs and graph dir exist
check_dir('./logs')
check_dir('./graphs')

format = '%(message)s'
dir_path = f"./logs/"
count = 1

for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        count += 1

filename = f'{count}'

logs = f'{dir_path}Game_{count}.log'


logging.basicConfig(level=logging.INFO, filename=logs, format=format)

'''
You can quit the game at any time by typing "quit" into the terminal
'''

class InfoSimulator:
    def __init__(self, uncert_ints: list, n: int, p: int, grey_proportion: int, simulate=False) -> None:
        self.social_network = list()
        self.red_agent = Agents.Red_Agent()
        self.blue_agent = Agents.Blue_Agent()
        self.grey_agent = Agents.Grey_Agent(grey_proportion)
        self.metrics = Metrics.Metrics()
        self.current_turn = ""
        self.num_turns = 0

        self.uncert_ints = uncert_ints
        self.n = n
        self.p = p
        self.grey_proportion = grey_proportion

        self.num_will_vote = 0
        self.num_not_vote = 0
        
        self.previous_change_toBlue = 0
        self.previous_change_toRed = 0
        self.before_interaction = 0 
        self.after_interaction = 0
        # Create a graph for modelling
        self.model = nx.Graph()
        self.social_network = self.create_green_agents(uncert_ints, n, p)
        self.update_vote_status()

        if not simulate:
            self.ask_for_players()

    def create_green_agents(self, uncernt_ints, n: int, p: list) -> list:
        social_network = list()
        # construct num_green of Green Agents
        for i in range(n):
            new_agent = Agents.Green_Agent(uncernt_ints, i)
            social_network.append(new_agent)

            # IF GREEN IS NOT VOTING IT IS A FOLLOWER OF RED
            # if new_agent.get_vote_status() == False:
            self.red_agent.connections.append(i)
            self.red_agent.increment_followers() #increment followers

            # BLUE HAS A CONNECTION TO EVERYONE
            self.blue_agent.connections.append(i)

        # Check for connections between green agents
        for i, agent in enumerate(social_network):

            for j in range(i+1, n):

                # When is j less than i we have already checked those connections
                # Thats why we start at  i+1

                agent_1_prob = agent.get_rand()
                agent_2_prob = social_network[j].get_rand()
                
                # check if agent has a connection
                # we can just compare one agent instead of two.
                # We should simulate what happens
                if (agent_1_prob < p) and (agent_2_prob < p):

                    # add to g for modelling
                    self.model.add_edge(i, j)

                    # add to agents adjlist
                    agent.add_connection(j)
                    social_network[j].add_connection(i)

        return social_network

    def add_connections(self):
        for i, agent in enumerate(self.social_network):
            conn_list = agent.get_connections()
            for conn in conn_list:
                self.g.add_edge(i, conn)


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

    
    def log_current_votes(self):
        logging.info(f"\t\tWill Vote: {self.num_will_vote}")
        logging.info(f"\t\tNot Vote: {self.num_not_vote}\n")


    def choose_first_move(self):
        # TODO: allow human players to choose 0 (heads) or 1(tails) 
        if rand.randint(0, 1) == 0:
            self.current_turn = "blue"
            self.red_agent.goingFirst = False
        else:
            self.current_turn = "red"
            self.blue_agent.goingFirst = True

        print(f"{self.current_turn} will go first!")


    def get_current_turn(self):
        return self.current_turn


    def set_current_turn(self, turn):
        self.current_turn = turn


    def get_num_turns(self):
        return self.num_turns


    def increment_turns(self):
        self.num_turns += 1


    def run(self):
        logging.info(f"Game Start:")
        logging.info(f"\tParameters: ")
        logging.info(f"\t\tUncertainty Intervals: [{self.uncert_ints[0]}, {self.uncert_ints[1]}]")
        logging.info(f"\t\tConnection Probability: [{self.n}, {self.p}]")
        logging.info(f"\t\tGrey Proportions: {self.grey_proportion}")

        try:
            # Randomly choose who goes first
            self.choose_first_move()
            logging.info(f"\t\tWill Vote: {self.num_will_vote}")
            logging.info(f"\t\tNot Vote: {self.num_not_vote}\n")
            logging.info(f"Turn: {self.num_turns+1}")
            self.metrics.save_uncert_dist(self.social_network, filename, "Start", (self.num_turns))
            

            finished = False

            while not finished:
                start = time.perf_counter()

                # Updates and prints gloabl values before each turn
                #self.metrics.display_connections(self.red_agent, self.blue_agent, self.social_network)
                #time.sleep(2)
                if self.get_current_turn() == "red":
                    logging.info("\tRed Agents Turn:")
                    print("\nRed Agents Turn...")
                    self.red_turn()
                    #time.sleep(2)
                    self.update_vote_status()
                    self.print_vote_status()
                    self.log_current_votes()
                    self.metrics.save_uncert_dist(self.social_network, filename, self.get_current_turn(), (self.num_turns//2)+1)
                    self.set_current_turn("blue")
                else:
                    logging.info("\tBlue Agents Turn:")
                    print("\nBlue Agents Turn...")
                    self.blue_turn()
                    #time.sleep(2)
                    self.update_vote_status()
                    self.print_vote_status()
                    self.log_current_votes()
                    self.metrics.save_uncert_dist(self.social_network, filename, self.get_current_turn(), (self.num_turns//2)+1)
                    self.set_current_turn("red")

                self.increment_turns()
                # Greens turn after red and blue have had their turns

                if self.get_num_turns() % 2 == 0 and not self.get_num_turns() == 0:
                    logging.info("\tGreen Agents Turn:")
                    print("\nGreen Agents are interacting....")
                    #time.sleep(2)
                    self.before_interaction = self.num_will_vote
                    self.green_turn()
                    self.after_interaction = self.num_will_vote
                    self.red_estimates()
                    self.blue_estimates()
                    self.update_vote_status()
                    self.print_vote_status()
                    self.log_current_votes()
                    self.metrics.save_uncert_dist(self.social_network, filename, "green", (self.num_turns//2))

                    if self.grey_agent.is_active():
                        logging.info("\tThe Grey Agent is making its move:")
                        print("\nGrey Agent Turn:")
                        #time.sleep(2)
                        self.grey_turn()
                        self.update_vote_status()
                        self.print_vote_status()
                        self.log_current_votes()
                        self.metrics.save_uncert_dist(self.social_network, filename, "grey", (self.num_turns//2))

                        # Grey only can be used once
                        self.grey_agent.set_active(False)
                
                    if self.blue_agent.get_energy() < 0 and self.get_num_turns() % 2 == 0:
                        finished = True
                        # Elapsed time end
                        end = time.perf_counter()
                        print("Finised in {:.3g} seconds".format(end-start))
                        self.check_winner()
                    else:
                        logging.info(f"Turn: {(self.num_turns//2)+1}")

                

        except KeyboardInterrupt:
            print("Ending game...")


    def check_winner(self):
        self.update_vote_status()
        self.print_vote_status()

        logging.info(f"Game finished at turn: {(self.num_turns//2)+1}")

        # save the graph of the green uncertainties at the end of the game
        self.metrics.save_uncert_dist(self.social_network, filename, "End",(self.num_turns//2)+1)

        final_num_will = 0
        final_num_not = 0
        final_num_uncertain = 0

        for agent in self.social_network:
            if agent.get_vote_status() == True and agent.get_uncert_value() < 0.00:
                final_num_will += 1
            elif agent.get_vote_status() == False and agent.get_uncert_value() < 0.00:
                final_num_not += 1
            else:
                final_num_uncertain += 1

        winner = ""
        if final_num_will > final_num_not:
            winner = "BLUE"
        elif final_num_will < final_num_not:
            winner = "RED"
        else:
            print("ITS A TIE!")
            logging.info(f'TIE')
            logging.info(f"Will Vote: {final_num_will}")
            logging.info(f"Not Vote: {final_num_not}")
            logging.info(f"Uncertain: {final_num_uncertain}")
            exit(0)

        print(f"{winner} AGENT WINS!!")
        logging.info(f'{winner}')
        logging.info(f"Will Vote: {final_num_will}")
        logging.info(f"Not Vote: {final_num_not}")
        logging.info(f"Uncertain: {final_num_uncertain}")
        exit(0)


    def ask_for_players(self):
        while True:
            option = input("Who do you want to play as? \n[1] Red\n[2] Blue\n[3] Both\n> ")

            print(option)
            try:
                if option.isdigit():
                    if int(option) > 3:
                        raise ValueError
                elif option == "quit":
                    raise Exception
                break
            except ValueError:
                print("This is not a valid Option. Please enter a valid option or type 'quit' to close the game")
            except Exception:
                print("Gracefully quiting game")
                exit(0)

        if int(option) == 1:
            self.red_agent.set_player(True)
        elif int(option) == 2:
            self.blue_agent.set_player(True)
        elif int(option) == 3:
            self.red_agent.set_player(True)
            self.blue_agent.set_player(True)
            
            return

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
                elif option == "":
                    raise ValueError
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
        option = -1

        if self.red_agent.get_player():
            option = self.user_input("red")
        else:
            pass
            option = self.minimaxRed(self.social_network, self.blue_agent, self.red_agent, 1, True)[0]
        
       # option = 2
        print("Choosing option :" + str(option))
        # Lose Followers
        lost = self.lose_followers(option) #change this to a percentage amountS

        # Change remaining green opinion
        amount = self.red_agent.broadcast(option)

        logging.info(f"\t\tUsing Option: {option}")
        logging.info(f"\t\tUncertainty: {amount}")
        logging.info(f"\t\tFollowers Lost: {lost}")
        
        
        if option > 0:
            self.previous_change_toRed = self.red_change_opinion(amount)
            #self.change_opinion(amount , False)


        return





    def blue_turn(self):
        print("Blue energy: " + str(self.blue_agent.get_energy()))
        
        option = -1

        # check if agent is AI or player
        if self.blue_agent.get_player():
            self.blue_agent.print_moves()
            option = self.user_input("blue")
        else: 
            option = self.minimaxBlue(self.social_network, self.blue_agent, self.red_agent, 2, True)[0]

        logging.info(f"\t\tUsing Option: {option}")

        if option == BLUE_OPTIONS["DEPLOY_GREY"]:
            self.deploy_grey_agent()
            self.blue_agent.set_used_grey()
            logging.info(f"\t\tDeployed Grey Agent: ({self.grey_agent.get_team_alignment()})")
        else:
            opinion_gain = self.blue_agent.get_opinion_gain(option)
            logging.info(f"\t\tUncertainty: {opinion_gain}")
            logging.info(f"\t\tCurrent Energy: {self.blue_agent.get_energy()}")

            # Change green opinion
            if option > 0:
                self.previous_change_toBlue = self.change_opinion(opinion_gain, True)

            # Lose Energy
            energy_lost = self.blue_agent.lose_energy(option)

            logging.info(f"\t\tEnergy Lost: {energy_lost}")
            


    def deploy_grey_agent(self):
        self.grey_agent.set_active(True)


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
        visited = []
        for agent in self.social_network:
            visited.append(agent)
            # Mingle with eachother and effect opinions
            is_voting = agent.get_vote_status()
            curr_agent_uncert = round(agent.get_uncert_value(),2)
            for connection in agent.connections:
                green_two = self.social_network[connection]
                if not green_two in visited:
                    green_two_uncert = round(green_two.get_uncert_value(),2)
                    green_two_opinion = green_two.get_vote_status()
                    #green 1 has -.5 not voting and green 2 has 0.3 as voting . Because green 1 is more certain then green 2 we get  -.5 - .8 = +.3. ANd we make green 2 -0.2 about not voting 
                    #green 1 has -.5 not voting and green 2 has -0.3 as voting . Because green 1 is more certain then green 2 we get  -.5 + .2 = -0.7. ANd we make green 2 -0.8 about not voting 

                    if curr_agent_uncert < green_two_uncert: #if current agent is more certain then its partner 
                        opinion_change = self.caculate_opinion_change(curr_agent_uncert, green_two_uncert) #find the difference between their uncertainties 
                        green_two.add_unert_values(opinion_change, is_voting)
                    else:
                        opinion_change = self.caculate_opinion_change(green_two_uncert, curr_agent_uncert)
                        agent.add_unert_values(opinion_change, green_two_opinion)
                    
                    
    def caculate_opinion_change(self, alpha: float, beta: float) -> float:
        '''
            Formula: 
                f(n) = 
                    (alpha + beta) if beta > 0.0
                    (alpha - beta) if beta <= 0.0
                    
            Params:
                alpha: float the uncertainty of the influencer
                beta: float the uncertainty of the agent being influenced
            
            Return:
                result: float value of how much alpha can influence beta
        '''
        #TODO: Nerf and buff this based on the number of green. This seems decent so *10 / num of people. 
        if beta < 0.00:
            return round((alpha + beta)*10/self.n, 2)
        else:
            return round((alpha - beta)*10/self.n, 2)


    def lose_followers( self , option: int):
        amount_lost = 0
        for i in self.red_agent.connections:
            probability = round(self.red_agent.Follower_Lost[option],2)
            node = self.social_network[i]
            #Voting already - more certain, higher chance of being lost 
            if node.get_vote_status(): #if they are voting
                uncertainty = node.get_uncert_value()
                probability -= uncertainty/8  #high uncertainty will raise the proability IF they are hella uncertain about voting they will stay 
            #Not Voting - more certain less chance of being lost 
            else: #if they are not voing
                uncertainty = node.get_uncert_value()
                probability += uncertainty/8  #high uncertainty will decrease the proability ( )
    
            if (rand.random()< probability):
                self.red_agent.remove_connections(i)
                self.red_agent.decrement_followers()
                amount_lost += 1
        return amount_lost


    def change_opinion(self, amount: float, is_voting: bool):
        '''
            This change opinion is used for blue, and grey agents as they can talk to everyone

        '''
        count = 0
        for agent in self.social_network:
            prev_voting = agent.get_vote_status()
            agent.add_unert_values(amount*2, is_voting)
            new_voting = agent.get_vote_status()

            if not prev_voting == new_voting:
                count += 1
        
        logging.info(f"\t\tOpinons Changed: {count}")
        print(f"Opinons Changed: {count}")
        return count

    def red_change_opinion(self, amount):
        is_voting = False
        count = 0

        for ssn in self.red_agent.get_connections():
            green_agent = self.social_network[ssn]
            prev_voting = green_agent.get_vote_status()
            green_agent.add_unert_values(amount*2, is_voting)
            new_voting = green_agent.get_vote_status()
            if not prev_voting == new_voting:
                count += 1
        logging.info(f"\t\tOpinions Changed: {count}")
        
        return count

    def red_estimates(self):
        self.red_agent.estimated_blue_energy -= round(self.previous_change_toBlue/5,2)  #can make this more adept
        previousPercent = (self.before_interaction - self.after_interaction)/self.n
        self.red_agent.estimated_influential_percentage = self.red_agent.estimated_influential_percentage + previousPercent

    def blue_estimates(self):
        self.blue_agent.estimated_red_loss -= round(self.previous_change_toRed,2) 
        previousPercent = ( self.after_interaction - self.before_interaction)/self.n
        self.blue_agent.estimated_influential_percentage = self.blue_agent.estimated_influential_percentage + previousPercent

    def evaluateState(self, greenNetwork, red, blue):
        #evaluate who is currently winning and return a point value 
        points = 0
        votes = 0
        nonVotes = 0
        for agent in greenNetwork:
            if agent.get_vote_status():
                points -= 5
                votes +=1 
            else: 
                points += 10
                nonVotes +1
        # points += int((100-blue.get_energy())/10) #less energy, better for red?

        points += red.get_followers()*6

        if nonVotes>votes:
            agression = 0 #starts conservative #agression can be on a scale of 0-50
            agression += round(red.estimated_blue_energy*1/100 ,2) # mildy the more energy blue hass
            agression -= round(red.estimated_influential_percentage * 10,2) #the less influential the followers are the more agressive it should play. Game is about having good followers

        else: #reds losing
            agression = 50
            agression -= round(red.estimated_blue_energy*1/100 ,2) #less energy blue has be more agressive
            agression -= round(red.estimated_influential_percentage *10,2) #be more agressive if you have a smaller percentage of influential voter
        points += int(math.sqrt(abs(agression)) * 0.4 )

        return points

    def evaluateBlue(self, greenNetwork, red, blue):
        #evaluate who is currently winning and return a point value 
        points = 0
        votes = 0
        nonVotes = 0
        for agent in greenNetwork:
            if agent.get_vote_status():
                points += 5
                votes +=1 
            else: 
                points -= 10
                nonVotes +1
        points += int(self.n/blue.get_energy())

        if nonVotes>votes:
            agression = 0 #starts conservative #agression can be on a scale of 0-50
            agression += round(blue.estimated_red_loss*1/100 ,2) # mildy the more energy blue hass
            agression -= round(blue.estimated_influential_percentage * 10,2) #the less influential the followers are the more agressive it should play. Game is about having good followers

        else: #reds losing
            agression = 50
            agression -= round(blue.estimated_red_loss*1/100 ,2) #less energy blue has be more agressive
            agression -= round(blue.estimated_influential_percentage *10,2) #be more agressive if you have a smaller percentage of influential voter
        points += int(math.sqrt(abs(agression)) * 0.4 )

        return points


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

    def simulate_red_lost(self, red, green, option):
        #will need to do a deepcopy agent and so that different routes could be taken.
        # will use AVERAGE amounts (possibly take into consideration, min and max interval if we change it from a flat amount. )
        for i in red.connections:
            probability = round(red.Follower_Lost[option],2)
            node = green[i]
            #Voting already - more certain, higher chance of being lost 
            if node.get_vote_status(): #if they are voting
                uncertainty = node.get_uncert_value()
                probability -= uncertainty/8  #high uncertainty will raise the proability IF they are hella uncertain about voting they will stay 
            #Not Voting - more certain less chance of being lost 
            else: #if they are not voing
                uncertainty = node.get_uncert_value()
                probability += uncertainty/8  #high uncertainty will decrease the proability ( )
    
            if (rand.random()< probability):
                red.remove_connections(i)
                red.decrement_followers()
        return red.broadcast(option, average = True) 
        

    def simulate_blue_energy(self, blueAgent, option):
        blueAgent.lose_energy(option, average = True)
        return blueAgent.get_opinion_gain(option, average = True)

    def simulate_green_turn(self, greenNetwork):
        visited = []
        for agent in greenNetwork:
            visited.append(agent)
            # Mingle with eachother and effect opinions
            is_voting = agent.get_vote_status()
            curr_agent_uncert = round(agent.get_uncert_value(),2)
            for connection in agent.connections:
                green_two =greenNetwork[connection]
                if not green_two in visited:
                    green_two_uncert = round(green_two.get_uncert_value(),2)
                    green_two_opinion = green_two.get_vote_status()
                    #green 1 has -.5 not voting and green 2 has 0.3 as voting . Because green 1 is more certain then green 2 we get  -.5 - .8 = +.3. ANd we make green 2 -0.2 about not voting 
                    #green 1 has -.5 not voting and green 2 has -0.3 as voting . Because green 1 is more certain then green 2 we get  -.5 + .2 = -0.7. ANd we make green 2 -0.8 about not voting 

                    if curr_agent_uncert < green_two_uncert: #if current agent is more certain then its partner 
                        opinion_change = self.caculate_opinion_change(curr_agent_uncert, green_two_uncert) #find the difference between their uncertainties 
                        green_two.add_unert_values(opinion_change, is_voting)
                    else:
                        opinion_change = self.caculate_opinion_change(green_two_uncert, curr_agent_uncert)
                        agent.add_unert_values(opinion_change, green_two_opinion)

        return


    def minimaxRed(self, green: list, blue: Agents.Blue_Agent, red: Agents.Red_Agent, depth: int, Maxteam: bool) -> tuple: 
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
            value = -math.inf
            choice =  rand.randint(0,5)
            for option in range(len(red.broadcast_options) -1 ): 
                #print(option)
                green_Copy = copy.deepcopy(green)
                red_Copy = copy.deepcopy(red)        
                opinion_change = self.simulate_red_lost(red_Copy, green_Copy, option)
                self.simulate_change_opinion(green_Copy, opinion_change, False)
                self.simulate_green_turn(green_Copy)

                new_score = self.minimaxRed(green_Copy, blue, red_Copy, depth-1, 0)
                if new_score[1] > value:
                    value = new_score[1]
                    if new_score[0] == -1:
                        choice = option
                    else:
                        choice = new_score[0]
            return (choice, value)
        
        else:
            value = math.inf
            choice =  rand.randint(0,5)
            for option in range(len(blue.opinion_gain)): 
                green_Copy = copy.deepcopy(green)
                blue_Copy = copy.deepcopy(blue)
                opinion_change = self.simulate_blue_energy(blue_Copy, option)
                self.simulate_change_opinion(green_Copy, opinion_change, True)
                self.simulate_green_turn(green_Copy)
                new_score = self.minimaxRed(green_Copy, blue_Copy, red, depth -1, 1)

                if new_score[1] < value:
                    value = new_score[1]
                    if new_score[0] == None:
                        choice = option
                    else:
                        choice = new_score[0]
            return (choice, value)
        
    def minimaxBlue(self, green: list, blue: Agents.Blue_Agent, red: Agents.Red_Agent, depth: int, Maxteam: bool) -> tuple: 
        #maxteam false - blues turn
        #Easier than adding more unecssary variables to copy and paste
        #Gamestate needs to be updated to be sent to the Minimax, should present copy of social network
        if self.isterminal(blue): #blue team is dead  checking gamestate, basically the only terminal node is if the blue is dead. 
            if self.RedWinning(green):
                return (-1,-100000000)
            else:
                return (-1,100000000)
        elif depth == (0):
            return (-1,self.evaluateBlue(green, red, blue))
        if not Maxteam:
            value = math.inf
            choice =  rand.randint(0,5)
            for option in range(len(red.broadcast_options)): 
                #print(option)
                green_Copy = copy.deepcopy(green)
                red_Copy = copy.deepcopy(red)        
                opinion_change = self.simulate_red_lost(red_Copy, green_Copy, option)
                self.simulate_change_opinion(green_Copy, opinion_change, False)
                self.simulate_green_turn(green_Copy)

                new_score = self.minimaxBlue(green_Copy, blue, red_Copy, depth-1, 0)
                if new_score[1] < value:
                    value = new_score[1]
                    if new_score[0] == -1:
                        choice = option
                    else:
                        choice = new_score[0]

            return (choice, value)
        
        else:
            value =  - math.inf
            choic =  rand.randint(0,5)
            for option in range(len(blue.opinion_gain) -1): 
                green_Copy = copy.deepcopy(green)
                blue_Copy = copy.deepcopy(blue)
                opinion_change = self.simulate_blue_energy(blue_Copy, option)
                self.simulate_change_opinion(green_Copy, opinion_change, True)
                self.simulate_green_turn(green_Copy)
                new_score = self.minimaxBlue(green_Copy, blue_Copy, red, depth -1, 1)

                if new_score[1] > value:
                    value = new_score[1]
                    if new_score[0] == -1:
                        choice = option
                    else:
                        choice = new_score[0]
            return (choic, value)
        


    def isterminal(self, blue):
        if blue.get_energy() == 0: #need to also check if they have a grey agent left still
            return True
        return False
        #check if blue is dead. 

    def RedWinning(self, network: list) -> bool:
        redFollowers = 0
        blueFollowers = 0
        for agent in network:
            if agent.get_vote_status():
                blueFollowers += 1
            else:
                redFollowers += 1
        return redFollowers > blueFollowers #winning move



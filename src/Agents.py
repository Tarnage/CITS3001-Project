import random as rand
from datetime import datetime

SEED_ONE = 1234
SEED_TWO = 4321


class Agent:
    def __init__(self, team):
        self.connections = list()
        self.team = team
        self.player = False # If True this agent is a human player if False it is AI
        return

    def set_player(self, is_player):
        self.player = is_player

    def get_player(self):
        return self.player

    def get_rand(self, uncert=[], uniform=False) -> float:
        '''
        If uniform is false (default) returns a random interval float 0 to 1
        If uniform is true, unertainty range must be passed to the function and will return a random float between uncernt_int[0] to uncernt_int[1]
        '''
        if uniform == True:
            # TODO: add check for valid input
            # round to 2 decimal places
            return round(rand.SystemRandom().uniform(uncert[0], uncert[1]), 2)
        else:
            return round(rand.random(), 2)

    def get_connections(self) -> list:
        return self.connections

    def add_connection(self, agent) -> None:
        self.connections.append(agent)

    def remove_connections(self, ind: int) -> None:
        self.connections.remove(ind)

    def get_team(self):
        return self.team


class Grey_Agent(Agent):
    def __init__(self, grey_proportion):
        self.team_alignment = self.set_team_alignment(grey_proportion)
        self.active = False
        self.uncert = -0.30
        super().__init__(team="grey")

    def set_team_alignment(self, proportion):
        num = self.get_rand()
        if num < proportion:
            return "red"
        else:
            return "blue" 

    def get_team_alignment(self):
        return self.team_alignment

    def set_active(self, input: bool):
        self.active = input

    def is_active(self):
        return self.active
    
class Red_Agent(Agent):
    def __init__(self):
        super().__init__(team="red")
        self.broadcast_options = [[0.00, 0.00], [-0.30, -0.10], [-0.50, -0.20], [-0.60, -0.30], [-0.70, -0.40], [-0.80, -0.60] ,[-0.80, -0.60]]
        self.Follower_Lost = [0.00, 0.05, 0.10, 0.15, 0.20, 0.25,0.30]
        self.followers = 0
        self.goingFirst = True
        self.estimated_blue_energy= 100
        self.estimated_influential_percentage = 0.5
        return

    def increment_followers(self):
        self.followers += 1

    def decrement_followers(self):
        self.followers -= 1

    def get_followers(self):
        return self.followers
    
    def print_moves(self):
        print("What would the Red Agent like to do:")
        print("[0] cost: Do nothing")
        print("[1] cost: 0-10'%' followers")
        print("[2] cost: 10-20'%' followers")
        print("[3] cost: 20-30'%' followers")
        print("[4] cost: 30-40'%' followers")
        print("[5] cost: 40-50'%' followers")

    def average_followers_lost(self, option: int) -> int:
        lost_followers = int(self.Follower_Lost[option] * self.followers) #gives average for simulation
        self.followers += lost_followers
        return lost_followers

    def broadcast(self, option: int, average = False) -> float:
        range = self.broadcast_options[option]
        amount = 0.0
        if average:
            amount = (range[0]+range[1])/2
        else:
            amount = self.get_rand(range, uniform= True)
        return round(amount,2)
    
    
        


class Blue_Agent(Agent):
    def __init__(self):
        self.energy = 100
        self.used_grey_agent = False
        self.opinion_gain = [[0.00, 0.00], [0.00, -0.20], [-0.10, -0.30], [-0.20, -0.40], [-0.30, -0.50], [-0.40, -0.50]]
        self.goingFirst = True
        self.estimated_red_loss = 0
        self.estimated_influential_percentage = 0.5
        super().__init__(team="blue")

    def get_energy(self) -> int:
        return self.energy

    def lose_energy(self, option: int, average = False) -> float:
        result_range = self.opinion_gain[option]
        if average:
            return (result_range[0]+result_range[1])/2

        energy_lost = self.get_rand(result_range, uniform=True)
        self.energy += int(energy_lost * 100 // 2)
        return int(energy_lost * 100 // 2)

    def print_moves(self):
        print("What would the Blue Agent like to do:")
        print("[0] cost: 0 energy: Do Nothing")
        print("[1] cost: 10-20 energy")
        print("[2] cost: 10-30 energy")
        print("[3] cost: 20-40 energy")
        print("[4] cost: 30-50 energy")
        print("[5] cost: 40-50 energy")

        if not self.used_grey():
            print("[6] cost: 0 energy: Deploy grey agent")
    
    def used_grey(self):
        return self.used_grey_agent

    def set_used_grey(self):
        self.used_grey_agent = True

    def get_opinion_gain(self, option: int, average = True) -> float:
        result_range = self.opinion_gain[option]
        if average:
            return round((result_range[0]+result_range[1])/2, 2)
        return round(self.get_rand(result_range, uniform=True), 2)

class Green_Agent(Agent):
    def __init__(self, uncert_ints, ssn):
        self.ssn = ssn # ssn is the social security number an int to index the green agent, in the social_network variable
        self.uncert = 0.00
        self.voting = bool
        self.set_uncerts(uncert_ints)
        super().__init__(team="green")

    def get_ssn(self):
        return self.ssn

    def get_uncert_value(self):
        return round(float(self.uncert), 2)

    def get_vote_status(self):
        return self.voting

    def set_vote_status(self, is_voting: bool):
        self.voting = is_voting

    def update_uncert(self, value: float):
        # max_min_value = 1.0

        # # if val is > 1.0
        # if value > max_min_value:
        #     self.uncert = max_min_value
        
        # # id val is < -1.0
        # elif value < -max_min_value:
        #     self.uncert = -max_min_value

        # # else its a valid value
        # else:
        if value < 0.00:
            self.uncert -= value
        else:
            self.uncert += value

    def set_uncerts(self, uncert: list):
        will_vote = self.get_rand(uncert, uniform=True)
        not_vote = self.get_rand(uncert, uniform=True)
        if will_vote < not_vote:
            self.set_vote_status(True)
            self.uncert = will_vote
        else:
            self.set_vote_status(False)
            self.uncert = not_vote

    def switching_sides(self, uncert: float):
        switchside  = False
        if rand.random() < uncert: 
            switchside = True
        return switchside


    def add_unert_values(self, value: float, is_voting: bool):
        #value is negative
        prev_voting = self.get_vote_status()
        # # Update uncertainty values
        # self.update_uncert(round(value, 2))

        # An agent is being influenced to change their voting status
        if not prev_voting == is_voting:

                                         #   if prev_uncert < 0.00: #if they are certain, then ADD the value  to make them more uncertain
            result = round((self.uncert - value),2)#make them more uncertain

            if result >= 1.00:
                self.uncert = 1.00 
            else:
                self.uncert = result
            
            if self.uncert> 0 and self.switching_sides(self.uncert): #if they are feeling uncertain there is a chance they switch sides
                self.set_vote_status(is_voting)
                self.uncert =round(-1 * self.uncert,2) #switch to the other side 



        else: #if they already are on the side
            result = round((self.uncert + value),2) #make them more certain

            if result <= -1.00:
                self.uncert = -1.00
            else:
                self.uncert = result

            # agent was unsure of their voting status before and now is sure 
        
                #print("Status Changed")
    
       # else:
            # The current green agent is being influenced by 
            # the side that they are currently on
            # if prev_uncert < 0.00:
            #     result = (self.uncert - value)

            #     if result <= -1.00:
            #         self.uncert = -1.00
            #     else:
            #         self.uncert = result
            # else:
            #     result = (self.uncert + value)

            #     if result >= 1.00:
            #         self.uncert = -1.00
            #     else:
            #         self.uncert = result
          #  pass
            

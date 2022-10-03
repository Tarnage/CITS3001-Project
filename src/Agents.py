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

    def set_player(self):
        self.player = True

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

    def set_active(self):
        self.active = True

    def is_active(self):
        return self.active
    
class Red_Agent(Agent):
    def __init__(self):
        super().__init__(team="red")
        return

    # def get_energy(self) -> int:
    #     return self.energy

    # def set_energy(self, new_energy: int) -> None:
    #     self.energy = new_energy


class Blue_Agent(Agent):
    def __init__(self):
        self.energy = 100
        self.used_grey_agent = False
        self.opinion_gain = [[0.00, 0.00], [0.00, 0.20], [0.10, 0.30], [0.20, 0.40], [0.30, 0.50], [0.40, 0.50]]
        super().__init__(team="blue")

    def get_energy(self) -> int:
        return self.energy

    def lose_energy(self, option: int) -> None:
        result_range = self.opinion_gain[option]
        energy_lost = self.get_rand(result_range, uniform=True)
        self.energy -= int(energy_lost * 100)

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

    def get_opinion_gain(self, option: int) -> float:
        result_range = self.opinion_gain[option]
        return self.get_rand(result_range, uniform=True)

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
        return self.uncert

    def set_uncerts(self, uncert: list):
        will_vote = self.get_rand(uncert, uniform=True)
        not_vote = self.get_rand(uncert, uniform=True)
        if will_vote() < not_vote():
            self.voting = True
            self.uncert = will_vote
        else:
            self.voting = False
            self.uncert = not_vote

    def add_unert_values(self, value: float, is_voting: bool):
        prev_voting = self.get_vote_status()
        prev_uncert = self.get_uncert_value()

        # Update uncertainty values
        self.uncert(round(self.uncert + value, 2))

        # An agent is being influenced to change their voting status
        if not is_voting == prev_voting:
            curr_uncert = self.uncert

            # agent was unsure of their voting status before and now is sure 
            if prev_uncert >= 0.00 and curr_uncert < 0.00:
                self.voting = is_voting
        
        else:
            # The current green agent is being influenced by 
            # the side that they are currently on 
            pass

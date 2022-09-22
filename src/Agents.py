import random as rand
from datetime import datetime

SEED_ONE = 1234
SEED_TWO = 4321


class Agent:
    def __init__(self, team):
        self.connections = list()
        self.team = team
        return

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
        super().__init__(team="grey")

    def set_team_alignment(self, proportion):
        return

    def set_active(self, status: bool):
        self.active = status

    def get_active(self):
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
        super().__init__(team="blue")

    def get_energy(self) -> int:
        return self.energy

    def lose_energy(self, energy: int) -> None:
        self.energy -= energy


class Green_Agent(Agent):
    def __init__(self, uncert_ints, ssn):
        self.ssn = ssn # ssn is the social security number an int to index the green agent, in the social_network variable
        self.will_vote = 0.0
        self.not_vote = 0.0
        self.voting = bool
        self.set_uncerts(uncert_ints)
        super().__init__(team="green")

    def get_ssn(self):
        return self.ssn
        
    def get_vote_status(self):
        return self.voting

    def get_will_vote(self):
        return self.will_vote

    def get_not_vote(self):
        return self.not_vote

    def set_uncerts(self, uncert: list):
        self.set_will_vote(self.get_rand(uncert, uniform=True))
        self.set_not_vote(self.get_rand(uncert, uniform=True))
        self.set_voting()

    def set_voting(self):
        # TODO: comparing float point numbers can add errors
        if self.get_will_vote() < self.get_not_vote():
            self.voting = True
        else:
            self.voting = False

    def set_will_vote(self, value: int):
        max_min_value = 1.0

        # if val is > 1.0
        if value > max_min_value:
            self.will_vote = max_min_value
        
        # id val is < -1.0
        elif value < -max_min_value:
            self.will_vote = -max_min_value

        # else its a valid value
        else:
            self.will_vote = value
 
    def set_not_vote(self, value: int):
        max_min_value = 1.0

        # if val is > 1.0
        if value > max_min_value:
            self.not_vote = max_min_value
        
        # id val is < -1.0
        elif value < -max_min_value:
            self.not_vote = -max_min_value

        # else its a valid value
        else:
            self.not_vote = value

    def add_vote(self, value : int):
        self.set_will_vote(self.will_vote + value)
    
    def add_not_vote(self, value : int):
        self.set_not_vote(self.not_vote + value)
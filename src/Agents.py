import random as rand
SEED = 1234
rand.seed(SEED)

class Agent:
    def __init__(self, team):
        self.connections = list()
        self.team = team
        return

    def get_prob_value(self) -> int:
        return rand.random()

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
    def __init__(self):
        self.will_vote = 0.0
        self.not_vote = 0.0
        self.voting = bool
        super().__init__(team="green")

    def get_will_vote(self):
        return self.will_vote

    def get_not_vote(self):
        return self.not_vote
    
    def get_side(self):
        return self.voting

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

    def current_side(self):
        if self.not_vote < self.will_vote:
            self.voting = True
        else:
            self.voting = False 

    def calculate_vote_status(self, interval: list):
        return
import random as rand
SEED = 1234
rand.seed(SEED)

class Agent:
    def __init__():
        return

    def get_prob_value(self) -> int:
        return rand.random()


class Grey_Agent(Agent):
    def __init__(self, grey_proportion):
        self.team_alignment = self.set_team_alignment(grey_proportion)

    def set_team_alignment(self, proportion):
        return


class Red_Agent(Agent):
    def __init__(self):
        self.energy = 100

    def get_energy(self) -> int:
        return self.energy

    def set_energy(self, new_energy: int) -> None:
        self.energy = new_energy


class Blue_Agent(Agent):
    def __init__(self):
        self.energy = 100

    def get_energy(self) -> int:
        return self.energy

    def set_energy(self, new_energy: int) -> None:
        self.energy = new_energy

        
class Green_Agent(Agent):
    def __init__(self):
        self.will_vote = 0.0
        self.not_vote = 0.0
        self.connections = list()

    def get_will_vote(self):
        return self.will_vote

    def get_not_vote(self):
        return self.not_vote

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

    def calculate_vote_status(self, interval: list):
        return

    def get_connections(self) -> list:
        return self.connections

    def add_connection(self, conn: int) -> None:
        self.connections.append(conn)
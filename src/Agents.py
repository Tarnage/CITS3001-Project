class Grey_Agent():
    def __init__(self, grey_proportion):
        self.team_alignment = self.set_team_alignment(grey_proportion)

    def set_team_alignment(self, proportion):
        return

class Red_Agent():
    def __init__(self):
        self.energy = 100


class Blue_Agent():
    def __init__(self):
        self.energy = 100


class Green_Agent():
    def __init__(self):
        self.will_vote = 0.0
        self.not_vote = 0.0
    
    def get_will_vote(self):
        return self.will_vote

    def get_not_vote(self):
        return self.not_vote

    def set_will_vote(self, value: int):
        self.will_vote = value

    def set_not_vote(self, value: int):
        self.not_vote = value

    def calculate_vote_status(self, interval: list):
        return
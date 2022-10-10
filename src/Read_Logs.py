import os

class Logs:
    def __init__(self, team) -> None:
        self.turns = 0
        self.team = team
        self.uncert = [0]
        self.followers = list()
        self.followers_gained = [0]
        self.followers_lost = [0]
        self.total_green = 0

    def init_followers(self, followers: int):
        self.followers.append(followers)

    def init_green(self, tot_green: int):
        self.total_green = tot_green

    def get_turns(self):
        return self.turns

    def get_team(self):
        return self.team

    def set_team(self, team: str):
        self.team = team

    def get_uncert(self, index: int):
        if index < len(self.uncert) and index >= 0:
            return self.uncert[index]
        else:
            print("Index Out of Bounds")

    def get_followers(self, index: int):
        # each index of the curr_follwers list represents the turn. i.e curr_follower[2] will return the followers at turn 2
        if index < len(self.uncert) and index >= 0:
            return self.uncert[index]
        else:
            print("Index Out of Bounds")

    def set_followers(self, followers: int):
        # each index of the curr_follwers list represents the turn. i.e curr_follower[2] will return the followers at turn 2
        self.followers.append(followers)

    def get_followers_lost(self, index: int):
        # each index of the curr_follwers list represents the turn. i.e curr_follower[2] will return the followers at turn 2
        if index < len(self.uncert) and index >= 0:
            return self.followers_lost[index]
        else:
            print("Index Out of Bounds")

    def set_followers(self, followers: int):
        # each index of the curr_follwers list represents the turn. i.e curr_follower[2] will return the followers at turn 2
        self.followers.append(followers)

    def set_total_green(self, input: int):
        self.total_green = input


class Read_Logs:
    def __init__(self) -> None:
        self.results = dict()


    def read_logs(self, log: str):

        red = Logs("red")
        blue = Logs("blue")
        green = Logs("green")
        grey = Logs("grey")

        with open(log, 'r') as input:
            
            files = input.readlines()

            index = 2
            length = len(files)

            while index < length:

                pass
    

    def read_all_logs(self, path: str):
        
        # Change the directory
        os.chdir(path)

        # iterate through all file
        for file in os.listdir():
            # Check whether file is in text format or not
            if file.endswith(".log"):
                file_path = f"{path}\{file}"
        
                # call read text file function
                self.read_logs(file_path)
        

if __name__ == "__main__":
    path = ".\logs\Game_21.log"
    log_reader = Read_Logs()

    log_reader.read_logs(path)
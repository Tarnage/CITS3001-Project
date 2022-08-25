from scipy.stats import binom
import matplotlib.pyplot as plt
import numpy as np
import random as rand
TEST_SEED = 1234
rand.seed(TEST_SEED)


# Green Agent Class
# We must approriatley apply random seeds

# Green Agent Class
# We must approriatley apply random seeds

class Green_Agent():
    def __init__(self, connection_prob: list):
        self.will_vote = 0.0
        self.not_vote = 0.0
        self.n, self.p = connection_prob[0], connection_prob[1]
    
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

    def get_prob_index(self) -> int:
        return rand.randint(0, self.n)

    def get_prob_value(self) -> int:
        # 1000 is chosen for 3 decimal precsion
        # this may cause precision bugs!.. 
        return rand.randint(0, 1000) / 1000


def create_green_agents(num_green: int, connect_prob: list) -> list:
    green_agents = list()
    green_adjlist = [ [] for _ in range(num_green)]



    binom_range = np.arange(0, connect_prob[0]+1)
    binomial_pmf = binom.pmf(binom_range, connect_prob[0], connect_prob[1])
    
    for i in range(num_green):
        new_agent = Green_Agent(connect_prob)
        green_agents.append(new_agent)

    
    for i, agent in enumerate(green_agents):

        for j in range(i+1, num_green):
            
            g_index = agent.get_prob_index()
            g_value = agent.get_prob_value()

            # check if agent has a connection
            if g_value < binomial_pmf[g_index]:

                if not j in green_adjlist[i]:
                    green_adjlist[i].append(j)
                    green_adjlist[j].append(i)


    return (green_agents, green_adjlist)



connection_prob = [10, 0.4]

num_green = 5

g_agents, g_adjlist = create_green_agents(num_green, connection_prob)

for i in g_adjlist:
    for j in i:
        print(f'{j} ', end="")
    print()
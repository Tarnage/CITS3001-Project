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

# Green Agent Class
# We must approriatley apply random seeds

class Green_Agent():
    def __init__(self, connection_prob: list):
        self.will_vote = 0.0
        self.not_vote = 0.0
        self.n, self.p = connection_prob[0], connection_prob[1]
        self.connections = list()
    
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
        return rand.randint(0, 100) / 100

    def get_connections(self) -> list:
        return self.connections

    def add_connection(self, conn: int) -> None:
        self.connections.append(conn)

def create_green_agents(num_green: int, connect_prob: list) -> list:
    green_agents = list()

    #green_adjlist = [ [] for _ in range(num_green)]

    # calculate bionomials
    binom_range = np.arange(0, connect_prob[0]+1)
    binomial_pmf = binom.pmf(binom_range, connect_prob[0], connect_prob[1])
    
    prob = (connect_prob[0] * connect_prob[1]) / 100

    # construct num_green of Green Agents
    for i in range(num_green):
        new_agent = Green_Agent(connect_prob)
        green_agents.append(new_agent)

    
    # Check for connections between green agents
    for i, agent in enumerate(green_agents):

        for j in range(i+1, num_green):

            # When is j less than i we have already checked those connections
            # Thats why we start at  i+1
            
            agent_1_prob = agent.get_prob_value()
            agent_2_prob = green_agents[j].get_prob_value()
            
            # check if agent has a connection
            if (agent_1_prob < prob) and (agent_2_prob < prob):
                agent.add_connection(j)
                green_agents[j].add_connection(i)

    return green_agents




connection_prob = [100, 0.4]

num_green = 20

g_agents = create_green_agents(num_green, connection_prob)

for i, agent in enumerate(g_agents):
    adj_list = agent.get_connections()
    print(f"Agent #{i}: ", end="")
    for j in adj_list:
        print(f'{j} ', end="")
    print()
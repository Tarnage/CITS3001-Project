from matplotlib import pyplot as plt
import networkx as nx
import seaborn as sns
import os, sys
import numpy as np

class Metrics:
    def __init__(self) -> None:
        return

    def print_green_adjlist(self, network_list):
        for i, agent in enumerate(network_list):
            adj_list = agent.get_connections()
            print(f"Agent #{i}: ", end="")
            for j in adj_list:
                print(f'{j} ', end="")
            print()

    def display_green_network(self, nx_graph: nx, display="graph"):
            # Print the number of connections a green agent has
            #print(nx.degree(nx_graph))

            if display == "graph":
                # print the current green network
                pos = nx.circular_layout(nx_graph)

                plt.clf()
                nx.draw(nx_graph, pos, with_labels=1)
                plt.show(block=False)
                plt.pause(0.01)
                

            if display == "distribution":
                # This plot should resemble a bionomoial distribution

                all_degrees = list(dict((nx.degree(nx_graph))).values())
                unique_degrees = list(set(all_degrees))
                unique_degrees.sort()
                nodes_with_degrees = list()

                for i in unique_degrees:
                    nodes_with_degrees.append(all_degrees.count(i))
                
                plt.plot(unique_degrees, nodes_with_degrees)
                plt.xlabel("Connections")
                plt.ylabel("No. of Green Agents")
                plt.title("Green Agent Connection Distribution")
                plt.show()
            
    def display_connections(self, red, blue, green):
        nx_graph = nx.Graph()
        nx_graph.add_node("RED")
        nx_graph.add_node("BLUE")

        for u, agent in enumerate(green):
            nx_graph.add_node(u)
            
            for v in agent.connections:
                nx_graph.add_edge(u, v)

        for v in red.connections:
            nx_graph.add_edge("RED", v)

        for v in blue.connections:
            nx_graph.add_edge("BLUE", v)

        # print the current green network
        pos = nx.circular_layout(nx_graph)

        plt.clf()
        nx.draw(nx_graph, pos, with_labels=1)
        plt.show(block=False)
        plt.pause(0.01)

    def save_uncert_dist(self, network: list, filename: str, player: str, turn: int) -> None:
        graphs_dir = f'./graphs/Game_{filename}'

        self.check_dir(graphs_dir)

        graph_dest = f'{graphs_dir}/Turn_{turn}-{player}'
        not_voting_list = []
        voting_list = []

        for green in network:
            value = round(green.get_uncert_value(), 2)
            voting = green.get_vote_status()

            if voting:
                voting_list.append(value)
            else:
                not_voting_list.append(value)

        fig, (ax1, ax2) = plt.subplots(1, 2)

        sns.histplot(not_voting_list, ax=ax1).set(title=f'Green Agents Not Voting = {len(not_voting_list)}', ylabel="Number of Green Agents", xlabel="Uncertainty")
        plt.tight_layout()

        sns.histplot(voting_list, ax=ax2).set(title=f'Green Agents Voting = {len(voting_list)}', ylabel="Number of Green Agents", xlabel="Uncertainty")
        plt.tight_layout()
        plt.savefig(f'{graph_dest}')

        plt.close("all")

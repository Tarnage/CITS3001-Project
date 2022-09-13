from matplotlib import pyplot as plt
import networkx as nx

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
            
    def display_red_connections(self, red):
        nx_graph = nx.Graph()
        nx_graph.add_node("Red")
        for i in red.connections:
            nx_graph.add_edge("Red", i)

        # print the current green network
        pos = nx.circular_layout(nx_graph)

        plt.clf()
        nx.draw_networkx(nx_graph, pos, with_labels=1)
        plt.show(block=False)
        plt.pause(0.01)
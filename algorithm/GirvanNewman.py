# -*- coding: utf-8 -*-
# Author: https://github.com/jywhy6/
# Reference: https://sikasjc.coding.me/2017/12/20/GN/

import networkx as nx
import matplotlib.pyplot as plt


class GirvanNewman:
    def __init__(self, G):
        self.G_copy = G.copy()
        self.G = G
        self.division = [[n for n in G.nodes()]]
        self.all_Q = [0.0]
        self.max_Q = 0.0
        self.div_len_at_max_Q = 0

    # Divide communities by number k
    def divByK(self, k):
        # Until there is no edge in the graph
        while len(self.G.edges()) != 0:
            # Find the edge with largest betweenness centrality
            max_cent_edge = max(
                nx.edge_betweenness_centrality(self.G).items(),
                key=lambda item: item[1])[0]
            # Remove the edge with largest betweenness centrality
            self.G.remove_edge(max_cent_edge[0], max_cent_edge[1])
            print("Removed an edge: (" + str(max_cent_edge[0]) + ", " +
                  str(max_cent_edge[1]) + ")")
            # List the the connected components
            # For undirected graphs, use nx.connected_components
            components = [
                list(c) for c in list(nx.weakly_connected_components(self.G))
            ]
            # Make sure a new component is generated before calculating Q
            if len(components) != len(self.division) and len(components) <= k:
                cur_Q = self.calcQ(components, self.G_copy)
                self.all_Q.append(cur_Q)
                self.division = components
                if cur_Q > self.max_Q:
                    self.max_Q = cur_Q
                    self.div_len_at_max_Q = len(self.division)
                # Remember to add group info
                self.addGroupInfo()
                self.toGml("GNoutput_" + str(len(self.division)) + "_" +
                           str(cur_Q) + ".gml")
                print('The current number of communites:', len(self.division))
                print('The current Q:', cur_Q)
        return self.division, cur_Q, self.all_Q

    # Draw the graph of Q and divided communities
    def drawQ(self):
        plt.plot([x for x in range(1, len(self.all_Q) + 1)], self.all_Q)
        plt.axvline(self.div_len_at_max_Q, color='black', linestyle="--")
        plt.axhline(self.max_Q, color='red', linestyle="--")
        plt.show()

    # Compute the modularity Q
    def calcQ(self, division, G):
        m = len(G.edges(None, False))
        a = []
        e = []
        # Attention: a includes communities' self connection
        # Please refer to the original paper
        for community in division:
            t = 0.0
            for node in community:
                t += len([x for x in G.neighbors(node)])
            a.append(t / (2 * m))

        for community in division:
            t = 0.0
            for i in range(len(community)):
                for j in range(len(community)):
                    if (G.has_edge(community[i], community[j])):
                        t += 1.0
            e.append(t / (2 * m))

        Q = 0.0
        for ei, ai in zip(e, a):
            Q += (ei - ai**2)
        return Q

    def addGroupInfo(self):
        num = 0
        nodegroup = {}
        for division in self.division:
            for node in division:
                nodegroup[node] = {'group': num}
            num = num + 1
        nx.set_node_attributes(self.G_copy, nodegroup)

    def toGml(self, file_name):
        nx.write_gml(self.G_copy, r"..\output\\" + file_name)


if __name__ == '__main__':
    # G = nx.read_edgelist(r"..\datasets\twitter_combined.txt")

    G = nx.DiGraph()
    cnt = 0
    with open(r"..\datasets\twitter_combined.txt", "r") as f:
        for line in f:
            tmp = line.split(" ")
            G.add_edge(int(tmp[0]), int(tmp[1].strip()))
            cnt = cnt + 1
            if (cnt > 30000):
                break

    print("Number of Nodes: " + str(G.number_of_nodes()))
    print("Number of Edges: " + str(G.number_of_edges()))

    gngraph = GirvanNewman(G)
    gngraph.divByK(20)
    gngraph.drawQ()
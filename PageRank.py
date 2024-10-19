# Import necessary libraries
import random
import csv
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Define empty lists and dictionary to store node and edge information
nodeList = []
edgeList = []
nodeCnt = {}

# Function to create a graph from a CSV file
def make_graph_from_csv(fileName):

    # Open the CSV file
    file = open(fileName, 'r')

    # Read CSV data
    data = csv.reader(file)
    next(data)  # Skip the header row

    # Create a directed graph object
    g = nx.DiGraph()

    # Iterate through each row in the CSV file
    for row in data:
        # Extract the source node (first column)
        p1 = row[1][0:11].upper()
        nodeList.append(p1)  # Add source node to the node list

        # Iterate through each target node (from the second column onwards)
        for i in row[2:]:
            if(i != ""):
                # Extract the target node (last 11 characters of the cell)
                p2 = i[-11:].upper()
                # Initialize count for the target node
                nodeCnt[p2] = 0
                # Add edge to the edge list
                edgeList.append((p1, p2))

    # Add nodes and edges to the graph
    g.add_nodes_from(nodeList)
    g.add_edges_from(edgeList)

    # Close the CSV file
    file.close()

    # Return the created graph
    return g

# Create a graph from the CSV file
Graph = make_graph_from_csv('impressionData.csv')

# Function to perform a random walk on the graph
def random_walk(graph):

    # Choose a random starting node
    random_node = random.choice(nodeList)

    # Iterate through the random walk process
    for i in range(100000):
        n = random.random()  # Generate a random number
        nodeCnt[random_node] += 1  # Increment the count for the current node
        if(list(Graph.neighbors(random_node)) == [] or n < 0.15):
            # If the current node has no neighbors or with a probability of 0.15, choose a new random node
            random_node = random.choice(nodeList)
            continue
        # Choose a random neighbor of the current node
        random_node = random.choice(list(Graph.neighbors(random_node)))

    # Sort the nodes based on their counts in descending order
    sorted_nodeList = dict(sorted(nodeCnt.items(), key=lambda item: item[1], reverse=True))
    print("the top leader is:", list(sorted_nodeList.keys())[0])  # Print the top leader
    return sorted_nodeList  # Return the sorted node list

random_walk()

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

# Function to perform link analysis
def linkAnalysis(adj_mat, node1, node2):
    # Remove node2 from the row corresponding to node1 and node1 from the column corresponding to node2 and store these row and column matrix in B and C respectively and store the adj mat after removing row n1 and col n2 in matrix A
    B = np.delete(adj_mat[node1], node2)
    C = np.delete(adj_mat[:, node2], node1)
    A = np.delete(adj_mat, node1, axis=0)
    A = np.delete(A, node2, axis=1)
    # Solve the equation xA = B using least squares method
    X, residuals, _, _ = np.linalg.lstsq(A.T, B, rcond=None)
    # Calculate the link analysis score
    return np.dot(X, C)

# Function to perform missing link analysis
def missingLinkAnalysis():
    # Initialize empty list to store missing links
    missing_Link = []
    c = 0  # Counter for missing links
    # Convert graph to adjacency matrix
    adj_mat = nx.adjacency_matrix(Graph).todense()
    # Perform random walk to get page rank
    pagerank = random_walk(Graph)
    pagerankKey_list = list(pagerank.keys())
    nodeList = list(nx.nodes(Graph))
    n = len(nodeList)
    # Iterate through each node in the graph
    for i in range(n):
        if(np.all(adj_mat[i] == 0)):
            # If the node has no outgoing edges
            for k in range(n):
                prob = .1 + .4*(1 - pagerankKey_list.index(nodeList[k])/(n-1))
                x = random.random()
                if(x <= prob):
                    # With a certain probability, add a link to another node
                    adj_mat[i][k] = 1
                    c += 1
                    missing_Link.append((nodeList[i], nodeList[k]))
                    print("Missing Link :", nodeList[i], '-', nodeList[k])
            continue
        # Iterate through each node pair to check for missing links
        for j in range(n):
            #checking if Aij is 1 or 0
            if(adj_mat[i][j] == 1 or i == j):
                continue
            a = linkAnalysis(adj_mat, i, j)
            # assigning 1 if link Analysis score is >0 else 0
            if(a > 0):
                a = 1
            if(a == 1):
                c += 1
                missing_Link.append((nodeList[i], nodeList[j]))
                print("Missing Link :", nodeList[i], '-', nodeList[j])
            adj_mat[i, j] = a
    # printing the obtained result
    print("Total number of missing links predicted : ", c)
    return adj_mat

missingLinkAnalysis()

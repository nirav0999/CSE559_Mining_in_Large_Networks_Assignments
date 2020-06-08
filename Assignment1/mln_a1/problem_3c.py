import networkx as nx
import csv
import matplotlib.pyplot as plt
import operator
import random


def readFile(filename):
	#Function to load the wikivote graph
	with open(filename) as file:
		lines = file.readlines()
		
		# Frst four lines are reudndant as they include no edges so removing those
		lines = lines[4:]

		# All the rest of the ines could be viewed as a csv file delimited by \t
		edges = csv.reader(lines,delimiter = "\t")
		return edges


def make_edge_list(edges):
	edge_list = []
	for edge in edges:
		node1 = int(edge[0])
		node2 = int(edge[1])
		edge_tup = (node1,node2) 
		rev_tup = (node2,node1)
		
		#Eliminate self edges
		if node1 != node2:
			if rev_tup not in edge_tup:
				edge_list.append(edge_tup)
	return edge_list



def graphInfo(graph,weighted = False):
	# Contains basic info of graph 
	nfnodes = graph.number_of_nodes()
	nfedges = graph.number_of_edges()
	nfselfLoops = graph.number_of_selfloops()
	print("Number of Vertices = ",nfnodes)
	print("Number of Edges = ",nfedges)
	print("Number of Self Loop Edges = ",nfselfLoops)
	print("Number of NON - self Loop Edges = ",nfedges - nfselfLoops)





#print(ERgraph.edges())
graph = nx.Graph()
edges = readFile("arxiv.txt")
edge_list = make_edge_list(edges)
graph.add_edges_from(edge_list)
graphInfo(graph)


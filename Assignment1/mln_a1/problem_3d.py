import networkx as nx
import csv
import matplotlib.pyplot as plt
import operator
import random
import numpy as np
import pickle


def loadPickleFile(filepath):
	print("Loading the pickle file from",filepath,"...........")
	pickle_in = open(filepath,"rb")
	example_dict = pickle.load(pickle_in)
	print("Loaded the pickle File")
	return example_dict

def dumpPickleFile(data,filepath):
	pickle_out = open(filepath,"wb")
	print("Dumping the Pickle file into ",filepath,"...........")
	pickle.dump(data, pickle_out)
	print("Dumped the pickle File")
	pickle_out.close() 

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
		edge_list.append(edge_tup)
	return edge_list


def make3a_Graph(n,L):
	#Function used in Q3B for documentation see problem 3a
	ERgraph = nx.Graph()
	print("Adding Nodes......")
	for node in range(n):
		ERgraph.add_node(node)
	print("Adding Edges......")
	edge_list = []
	for edge in range(L):
		#print(edge)
		RandomNumber1 = 0
		RandomNumber2 = 0
		tup = (RandomNumber2,RandomNumber1)
		rev_tup = (RandomNumber1,RandomNumber2)

		while(RandomNumber2 == RandomNumber1 or (tup in edge_list) or (rev_tup in edge_list)):
			RandomNumber1 = random.randint(0,n)
			RandomNumber2 = random.randint(0,n)
			tup = (RandomNumber2,RandomNumber1)
			rev_tup = (RandomNumber1,RandomNumber2)

		edge_list.append(tup)

		if edge % 1000 == 0:
			print("Adding edge between ",RandomNumber1,"and",RandomNumber2,"--------",edge)
		
		ERgraph.add_edge(int(RandomNumber1),int(RandomNumber2))
	return ERgraph

def make3b_Graph(n):
	#Function used in Q3B for documentation see problem 3B
	ERgraph = nx.Graph()
	print("Adding Nodes......")
	for node in range(n):
		ERgraph.add_node(node)

	print("Making a circle with consecutive edges.....")
	
	ERgraph.add_edge(0,n-1)
	for node in range(1,n - 1):
		ERgraph.add_edge(node-1 ,node)

	print("Number of Edges 1 = ",ERgraph.number_of_edges())
	print("Making a circle with bouncing edges.....")
	
	ERgraph.add_edge(1,n-1)
	ERgraph.add_edge(0,n-2)

	for node in range(n-3):
		ERgraph.add_edge(node,node + 2)

	print("Adding Random Edges......")
	print("Number of Edges 2 = ",ERgraph.number_of_edges())

	for edge_no in range(4000):
		RandomNumber1 = random.randint(0,n)
		RandomNumber2 = random.randint(0,n)
		while(RandomNumber2 == RandomNumber1 or ERgraph.has_edge(int(RandomNumber1),int(RandomNumber2)) == True):
			RandomNumber1 = random.randint(0,n)
			RandomNumber2 = random.randint(0,n)
		if edge_no % 1000 == 0:
			print("Adding edge between ",RandomNumber1,"and",RandomNumber2,"--------",edge_no)
		ERgraph.add_edge(int(RandomNumber1),int(RandomNumber2))

	print("Number of Edges 3 = ",ERgraph.number_of_edges())
	return ERgraph

def make3c_graph():
	#Function used in Q3B for documentation see problem 3c
	graph = nx.Graph()
	edges = readFile("arxiv.txt")
	edge_list = make_edge_list(edges)
	graph.add_edges_from(edge_list)
	return graph	

def make_dist(arr):
	dist = {}
	for tup in arr:
		degree = tup[1]
		if degree not in dist:
			dist[degree] = 1
		else:
			dist[degree] += 1
	return dist


def make_degree_dist_graph(graph,color = 'r',label = 'label'):
	degrees = graph.degree(weight = None)
	degree_dist = make_dist(degrees)

	degrees = []
	counts = []
	degree_dist1 = sorted(degree_dist.keys())
	
	for t in degree_dist1:
		degree = t
		#count = t[1]
		count = degree_dist[t]
		#print(t,count)
		counts.append(count)
		degrees.append(degree)


	log_degrees = np.log(degrees)
	log_counts = np.log(counts)

	#return log_degrees,log_counts
	plt.scatter(log_degrees[1:],log_counts[1:],c = color,marker='X',label=label)

	

def graphInfo(graph,weighted = False):
	print("Number of Vertices = ",graph.number_of_nodes())
	print("Number of Edges = ",graph.number_of_edges())
	print("Number of Connected Components = ",nx.number_connected_components(graph))
	#print("Average Degree = ",nx.average_degree_connectivity(graph))
	if weighted  == False:
		print("Size of Unweighted Graph = ",graph.size(weight = None))
	else:
		print("Size of Weighted Graph = ",graph.size(weight = "weight"))
		averageWeightedDegree = nx.average_degree_connectivity(graph,weight = "weight")
		print("Average Weighted Degree = ",averageWeightedDegree)


p3a_graph = loadPickleFile("problem_3a_graph.pkl")#make3a_Graph(5242,14484)
make_degree_dist_graph(p3a_graph,'r',"3a")
p3b_graph = loadPickleFile("problem_3b_graph.pkl")#make3b_Graph(5242)
make_degree_dist_graph(p3b_graph,'b',"3b")
p3c_graph = make3c_graph()
make_degree_dist_graph(p3c_graph,'g',"3c")


#Makes te comparision Graph of the three
plt.title("Degree Distribution Comparision")
plt.xlabel("Degree - log")
plt.ylabel("Number of nodes - log")
plt.legend()
plt.savefig("Graphs/3d/Comparision.png")
plt.show()









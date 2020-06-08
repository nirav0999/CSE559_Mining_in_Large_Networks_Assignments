import networkx as nx
import csv
import matplotlib.pyplot as plt
import operator
import math

def readFile(filename):
	#Function to load the wikivote graph
	with open(filename) as file:
		lines = file.readlines()

		# All the rest of the ines could be viewed as a csv file delimited by \t
		edges = csv.reader(lines,delimiter = "\t")
		return edges


def make_edge_list(edges):
	#Make Edge List
	edge_list = []
	for edge in edges:
		node1 = int(edge[0])
		node2 = int(edge[1])
		edge_tup = (node1,node2) 
		edge_list.append(edge_tup)
	return edge_list


def get_largest_weakly_connected_component(DG):
	# Makes the largest Weakly connected COmponent component of the graph
	largest_weak_connected_nodes = max(nx.weakly_connected_components(DG), key=len)
	largest_weak_connected_graph = DG.subgraph(largest_weak_connected_nodes)
	return largest_weak_connected_graph


def get_in_neighbours(node,graph):
	# Returns a list of all inneighbors of  the specified nodes
	in_edges = graph.in_edges(node)
	in_neighbors = []
	for in_edge in in_edges:
		node = in_edge[0]
		in_neighbors.append(node)
	return in_neighbors

def get_out_neighbors(node,graph):
	# Returns a list of all outneighbors of the specified nodes
	out_edges = graph.out_edges(node)
	out_neighbors = []
	for out_edge in out_edges:
		node = out_edge[1]
		out_neighbors.append(node)
	return out_neighbors


def authUpdateRule(node,graph):
	#neighbors = graph.neighbors(node)
	out_edges(nbunch=None, keys=False, data=False)



def getL1norm(old_dict,new_dict):
	# COmputes the L1 norm
	l1norm = 0
	for v in old_dict:
		l1norm += abs(old_dict[v] - new_dict[v])
	return l1norm/len(old_dict)

def getL2norm(old_dict,new_dict):
	# COmputes the L12norm
	l2norm = 0
	for v in old_dict:
		l2norm += abs(old_dict[v] - new_dict[v])**2
	l2norm = l2norm ** (1/2)
	return l2norm/len(old_dict)


def normalize_dictionary(dict1):
	# NOrmalizes the dictionary with the sum of it's values
	norm = sum(dict1.values())
	for v in dict1:
		dict1[v] = dict1[v]/norm
	return dict1


def HITS(G,max_iters,tol):
	hub_scores = {}
	authority_scores = {}
	prev_hub_scores = {}
	prev_authority_scores = {}
	nodes = G.nodes()
	
	# Initialzing Hub and Authority Scores
	for node in nodes:
		hub_scores[node] = 1/len(nodes)
		authority_scores[node] = 1/len(nodes)
		prev_hub_scores[node] =  1/len(nodes)
		prev_authority_scores[node] = 1/len(nodes)
	

	for iter_no in range(max_iters):
		print("Iteration Number ",iter_no)
		#----------------Authority Scores Updates----------------
		for node1 in nodes:
			in_neighbors_list = get_in_neighbours(node1,G) 
			for in_neighbor in in_neighbors_list:
				authority_scores[node1] += hub_scores[in_neighbor]

		#--------------Hub Scores Updates----------------
		
		for node1 in nodes:
			out_neighbors_list = get_out_neighbors(node1,G) 
			for out_neighbor in out_neighbors_list:
				hub_scores[node1] += authority_scores[out_neighbor]

		#--------------------Normalizing---------------
		a_norm = max(authority_scores.values())
		print("a_norm = ",a_norm)
		for node1 in nodes:
			authority_scores[node1] = authority_scores[node1]/a_norm

		h_norm = max(hub_scores.values())
		print("h_norm = ",h_norm)
		for node1 in nodes:
			hub_scores[node1] = hub_scores[node1]/h_norm
		
		#---------------Clauclating L1 norm----------------------------------
		L1_HubScore = getL1norm(prev_hub_scores,hub_scores)
		print("L1 norm Hub Score = ",L1_HubScore)
		
		if L1_HubScore < tol:
			break

		for v in prev_hub_scores:
			prev_hub_scores[v] = hub_scores[v]

	hub_scores = normalize_dictionary(hub_scores)
	authority_scores = normalize_dictionary(authority_scores)
	return hub_scores,authority_scores


#Loaded a Empty directed Graph from networkx 
DG = nx.DiGraph()
edges = readFile("so.txt")
edge_list = make_edge_list(edges)

# Adding edges to directed graph
DG.add_edges_from(edge_list)


print("Computing Library HITS ......")
(hubs,authorities) = nx.hits(DG, max_iter = 100, tol = 1e-10, nstart = None, normalized = True)

print("Computing Self Made HITS ......")
h,a = HITS(DG,500,1e-10)

#Soring the hub scores
hub_scores = sorted(h.items(), key=lambda x: x[1], reverse=True)
aut_score = sorted(a.items(), key=lambda x: x[1], reverse=True)



print("-------TOP 5 HUB SCORES---------------")
for i in range(5):
	print(hub_scores[i])

print("-------TOP 5 AUTHORITY SCORES---------------")
for i in range(5):
	print(aut_score[i])

h_l2 = getL2norm(hubs,h)
a_l2 = getL2norm(authorities,a)

print("The L2 normalization Difference is ",
print("Hub Scores = ",h_l2)
print("Authority Scores = ",a_l2)


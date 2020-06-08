import networkx as nx
import csv
import matplotlib.pyplot as plt
import operator
import numpy as np

def readFile(filename):
	#Function to load the wikivote graph
	with open(filename) as file:
		lines = file.readlines()

		# All the rest of the ines could be viewed as a csv file delimited by \t
		edges = csv.reader(lines,delimiter = "\t")
		return edges


def make_edge_list(edges):
	# Making a Well - defined edge list
	edge_list = []
	for edge in edges:
		node1 = int(edge[0])
		node2 = int(edge[1])
		edge_tup = (node1,node2) 
		edge_list.append(edge_tup)
	return edge_list


def get_largest_weakly_connected_component(DG):
	# Get the largesr Weakly Connected Components 

	#Nodes of the Largest Connected Subgraph
	largest_weak_connected_nodes = max(nx.weakly_connected_components(DG), key=len)
	
	#Makking the Largest Weakly connected component subgraph 
	largest_weak_connected_graph = DG.subgraph(largest_weak_connected_nodes)
	return largest_weak_connected_graph

def max_val(pageranks):
	# COmputes the max pagerank score and the nodeID 
	max_pagerank = 0
	max_i = 0
	for v in pageranks:
		pagerank = pageranks[v]
		if pagerank > max_pagerank:
			max_pagerank = pagerank
			max_i = v
	return max_i


def make_distribution(pageranks):
	# Given a pagerank dictionary , computes it's distribution
	pagerank_distribution = {}


	#Making the dictionary
	for v in pageranks:
		pagerank = pageranks[v]
		if pagerank not in pagerank_distribution:
			pagerank_distribution[pagerank] = 1
		else: 
			pagerank_distribution[pagerank] += 1

	#Soring the PageRank List
	pagerank_values = sorted(pagerank_distribution.keys())
	#print(pagerank_values)

	pagerank_counts = []

	for pagerank_v in pagerank_values:
		pagerank_count = pagerank_distribution[pagerank_v]
		pagerank_counts.append(pagerank_count)
		#print(pagerank_v,pagerank_count)


	return pagerank_distribution,pagerank_values,pagerank_counts


#--------------------------------MULTI GRaph Assumptions----------------------------------------
print("If considered a Multi Di Graph ------")
#Loaded a Empty directed Graph from networkx 
DG = nx.MultiDiGraph()
edges = readFile("so.txt")
edge_list = make_edge_list(edges)

# Adding edges to directed graph
DG.add_edges_from(edge_list)

print("Number of weakly connected components = ",nx.number_weakly_connected_components(DG))
print("Number of strongly connected components = ",nx.number_strongly_connected_components(DG))

largest_weakly_connected_component = get_largest_weakly_connected_component(DG)

nfnodes = largest_weakly_connected_component.number_of_nodes()
nfedges = largest_weakly_connected_component.number_of_edges()

print("Number of Vertices in largest_weak_connected_graph = ",nfnodes)
print("Number of Edges in largest_weak_connected_graph = ",nfedges)

#----------------------------------------------------------------------------------------------------------


print("If NOT considered a Multi Di Graph ------")
#Loaded a Empty directed Graph from networkx 
DG = nx.DiGraph()
edges = readFile("so.txt")
edge_list = make_edge_list(edges)

# Adding edges to directed graph
DG.add_edges_from(edge_list)

print("Number of weakly connected components = ",nx.number_weakly_connected_components(DG))
print("Number of strongly connected components = ",nx.number_strongly_connected_components(DG))

largest_weakly_connected_component = get_largest_weakly_connected_component(DG)

nfnodes = largest_weakly_connected_component.number_of_nodes()
nfedges = largest_weakly_connected_component.number_of_edges()

print("Number of Vertices in largest_weak_connected_graph = ",nfnodes)
print("Number of Edges in largest_weak_connected_graph = ",nfedges)

#Computing Pageranks ....
pageranks = nx.pagerank(DG, alpha=0.85, personalization=None, max_iter=100, tol=1e-06, nstart=None, weight = 'weight', dangling=None)

# Max Pagerank Score
max_pagerank_score_node = max_val(pageranks)
print("Node with the highest Pagerank Score is = ",max_pagerank_score_node)

#PageRank Distribution
pagerank_distribution,pagerank_values,pagerank_counts = make_distribution(pageranks)

plt.scatter(pagerank_values,pagerank_counts,c = 'red',marker = 'X')
plt.title("PageRank Distribution plot on log log scale")
plt.xlabel("PageRank Value - log scale")
plt.ylabel("Number of Nodes  log scale ")
#plt.savefig("Graphs/2a/PageRank_Distribution_plot_normal_scale.png")
plt.show()


print("Computing HITS Algorithm....")
# Library HITS 
(hubs,authorities) = nx.hits(DG, max_iter = 100, tol = 1e-08, nstart=None, normalized=True)
print("Computed Hubs and AUthorities Scores")

# Sorting the Hub Scores and Authorities Scores
print("Sorting Hubs Scores........")
all_hubs = sorted(hubs.items(), key = operator.itemgetter(1),reverse = True)
print("Sorting Authorities Scores....")
all_authorities = sorted(authorities.items(), key=operator.itemgetter(1),reverse = True)

#-----------------------------------------------------------------------------------------------------
print("--------------------TOP 5 Hubs------------------")
for i in range(5):
	hub = all_hubs[i][0]
	hub_val = all_hubs[i][1]
	print(str(i+1),"Node = ",hub,"Hub_Score = ",hub_val)

print("--------------------TOP 5 Authority-------------------")
for j in range(5):
	authority = all_authorities[j][0]
	authority_val = all_authorities[j][1]
	print(str(j+1),"Node = ",authority,"Authority_Score = ",authority_val)




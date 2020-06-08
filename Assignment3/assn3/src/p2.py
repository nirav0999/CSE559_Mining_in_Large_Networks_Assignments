import networkx as nx
import basic_functions
import graph_functions
import math
import random
import operator
import matplotlib.pyplot as plt
import numpy as np

def BFS(source,G):
	
	#Count nf shortest path
	count_nf_shortest_path = {}

	#Visited Vetices
	visited = {}

	#Length of the Shortest Path
	shortest_path_length = {}

	#Parent Set
	parent_set = {}

	#Levels of the tree
	level = {}

	# Initialize all dictionaries
	for node in G.nodes():
		visited[node] = False
		count_nf_shortest_path[node] = 0
		shortest_path_length[node] = math.inf
		parent_set[node] = []
		level[node] = math.inf

	# Initializing
	visited[source] = True
	shortest_path_length[source] = 0
	count_nf_shortest_path[source] = 1
	level[source] = 0

	#Queue for BFS
	queue = []
	queue.append(source)

	while queue:
		
		#POping from BFS
		source = queue.pop(0) 

		for neighbor in G.neighbors(source):

			if visited[neighbor] == False:
				# If vertex is NOT VISTED
				shortest_path_length[neighbor] = shortest_path_length[source] + 1
				count_nf_shortest_path[neighbor] = count_nf_shortest_path[source]
				visited[neighbor] = True
				parent_set[neighbor].append(source)
				level[neighbor] = level[source] + 1
				queue.append(neighbor)
			
			else:
				if shortest_path_length[neighbor] == shortest_path_length[source] + 1:
					# If vertex is VISITED and the new path length to current max path length
					count_nf_shortest_path[neighbor] += count_nf_shortest_path[source]
					parent_set[neighbor].append(source)

				elif shortest_path_length[neighbor] > shortest_path_length[source] + 1:
					# If vertex is VISITED and the new path length is shorter than max path length
					shortest_path_length[neighbor] = shortest_path_length[source] + 1
					count_nf_shortest_path[neighbor] = count_nf_shortest_path[source]
					parent_set[neighbor] = [source]

		

	return count_nf_shortest_path,shortest_path_length,parent_set,level


def make_tree(G,source,parent_set):
	tree = nx.Graph()
	for v in parent_set:
		if v != source:
			arr = parent_set[v]
			if len(arr) == 1 and arr[0] == source:
				tree.add_edge(source,v)
			else:
				tree.add_edge(arr[0],v)
	return tree



def calc_edge_dependencies(G,source,parent_set,level,nf_shortest_path,levels,betweenness):
	
	#nodes_and_degrees = sortNodesByDegree(tree,weight = "weight",reverse = False)
	leaves = []
	levels1 = {}
	delta = {}
	dependencies = {}

	for v in levels:
		level = levels[v]
		if level not in levels1: 
			levels1[level] = [v]
		else:
			levels1[level].append(v)

	for node in G.nodes():
		delta[node] = 0

	for edge in G.edges():
		dependencies[edge] = 0

	levels2 = list(levels1.keys())
	levels2.sort(reverse = True)
	

	for level in levels2:
		nodes_at_that_level = levels1[level]
		for node in nodes_at_that_level:

			for parent in parent_set[node]:

				c = (float(nf_shortest_path[parent])/nf_shortest_path[node]) * (1 + delta[node])
				
				if (node,parent) in dependencies:
					dependencies[(node,parent)] += c
				else:
					dependencies[(parent,node)] += c
				
				delta[parent] += c
	

	return dependencies


# Check if maximum value is greater 
def check_algo2(betweenness,c = 5,n = 1000):
	max_betweenness = max(betweenness.items(), key = operator.itemgetter(1))[1] 
	if max_betweenness >= c*n:
		return True
	return False


# Generate Random Set
def generate_random_set(n,set_size):
	random_arr = []
	for i in range(set_size):
		random_arr.append(random.randint(0,set_size))
	return random_arr


n = 1000
#Making Graph
G = nx.barabasi_albert_graph(n,4)

#Algo 1 initial Between ness values
betweenness = {}
for edge in G.edges():
	betweenness[edge] = 0

#Algo 1 - Between ness
for source in G.nodes():
	nf_shortest_path,shortest_path_length,parent_set,level = BFS(source,G)
	dependencies = calc_edge_dependencies(G,source,parent_set,level,nf_shortest_path,level,betweenness)
	for edge in betweenness:
		betweenness[edge] += dependencies[edge]

#Algo 2 initial Between ness values
betweenness2 = {}
for edge in G.edges():
	betweenness2[edge] = 0

#Genrating a random array with replacement
random_arr = generate_random_set(n,set_size = int(n/10))
c = 5 

#Final Betweenness values
final_betweenness = {}

#Algorithm 2 - Estimate Betweenness
for source_no,source in enumerate(random_arr):
	
	nf_shortest_path,shortest_path_length,parent_set,level = BFS(source,G)
	
	dependencies = calc_edge_dependencies(G,source,parent_set,level,nf_shortest_path,level,betweenness2)
	
	for edge in betweenness2:
		betweenness2[edge] += dependencies[edge]
	
	k = source_no + 1

	# Check Maximum 
	if check_algo2(betweenness2,c,n):
		break

#  Normalize Edge Betweenness
for edge in betweenness2:
	final_betweenness[edge] = (n * betweenness2[edge])/k


#Calculating the Avg Difference between estimated and exact between ness centrality

diff = 0
for e in betweenness:
	diff += abs(betweenness[e] - final_betweenness[e])
print("Average Error = ",diff/len(betweenness))

# diff = 0
# for e in betweenness[50:-50]:
# 	diff += abs(betweenness[e] - final_betweenness[e])
# print("Average Error = ",diff/len(betweenness))



# Make the Graph
sorted_exact = list(betweenness.values())
sorted_estimate = list(final_betweenness.values())
ex = []
es = []
sorted_exact.sort(reverse = True)
sorted_estimate.sort(reverse = True)

# print(sorted_exact)
# print(sorted_estimate)


# We calculate Normalized Error per 50 items in the array
for i in range(0,len(sorted_exact),50):
	diff = 0
	
	for pos in range(i,i+50):
		if pos < len(sorted_exact):
			ex.append(sorted_exact[pos])
			es.append(sorted_estimate[pos])
			diff += abs(sorted_exact[pos] - sorted_estimate[pos])/max(sorted_exact[pos],sorted_estimate[pos])
	
	print(i,i+50,diff)

ex = np.log(ex)
es = np.log(es)

plt.scatter(np.arange(1,len(ex)+1),ex,label = "Exact Betweenness",color = 'b')
plt.scatter(np.arange(1,len(es)+1),es,label = "Estimated Betweeness",color = 'r')
plt.xlabel("Position")
plt.ylabel("log(Centrality)")
plt.title("Comparison between Exact and Estimate Centrality")
plt.legend()
plt.show()
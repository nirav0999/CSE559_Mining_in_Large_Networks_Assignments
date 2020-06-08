import networkx as nx
import csv
import numpy as np
import heapq

def appendToCSV(filepath,row):
	with open(filepath,"a",buffering = 1) as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(row)

def openCSVfile(filepath):
	with open(filepath,"r") as csvfile:
		rows =  csv.reader(csvfile,delimiter = "\t")
		return list(rows)

def loadGraph():
	rows = openCSVfile(filepath)
	nodes = set([])
	new_rows = []
	for row in rows:
		node1 = int(row[0])
		node2 = int(row[1])
		new_rows.append((node1,node2))
	MDGraph = nx.MultiDiGraph(new_rows)	
	return MDGraph 

def makeTransitionMatrix(graph):
	w, h = 100,100;
	Matrix = [[0 for x in range(w)] for y in range(h)]

	for node1 in range(100):
		for node2 in range(100):
			
			#Nfedges between 2 nodes from u to v
			nfedges1_2 = graph.number_of_edges(node1 + 1,node2  +1)
			
			#Outdegree of node 
			outdegree = graph.out_degree(node1 + 1)

			#Filling the score in transition matrix
			initialPageRankScore = float(nfedges1_2)/float(outdegree)
			Matrix[node2][node1] = initialPageRankScore

	return Matrix 



def pageRank(MDGraph,max_iter = 40,beta = 0.8):

	#Inititializing PageRank and ones array
	PageRankScores = []
	ones = []
	nodes = MDGraph.nodes()
	n = len(nodes)

	#Initializing PageRank Scores
	for i in range(len(nodes)):
		PageRankScores.append(1/n)
		ones.append(1)

	#Making Transition Matrix and converting to numpy array
	PageRankScores = np.array(PageRankScores,dtype = 'float64')
	ones = np.array(ones,dtype = 'float64')
	transition_matrix = np.array(makeTransitionMatrix(MDGraph),dtype = 'float64')

	#Running for 40 iterations
	for iter_no in range(max_iter):
		#Pagerank Algorithm
		PageRankScores =  (1 - beta)/n * ones + beta * np.dot(transition_matrix,PageRankScores.T) 
		PageRankScores = PageRankScores.T
		#print(PageRankScores)

	return np.array(list(PageRankScores.flatten()))

filepath = "../Data/graph.txt"
MDGraph = loadGraph()
PageRankScores = pageRank(MDGraph)

# Printing Bottom 5 Scores
x = np.argsort(PageRankScores)

print("---------------------- Bottom 5 Scores -----------------------------")
print("ID","Score")
for k in x[:5]:
	print(k + 1,PageRankScores[k])



# Printing Top 5 Scores
x = x[::-1]
print("---------------------- Top 5 Scores -----------------------------")
print("ID","Score")
for k in x[:5]:
	print(k + 1,PageRankScores[k])

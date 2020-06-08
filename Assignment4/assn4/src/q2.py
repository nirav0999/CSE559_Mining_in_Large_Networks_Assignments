# import basic_functions
# import graph_functions
import networkx as nx
import matplotlib.pyplot as plt
from node2vec import Node2Vec
import basic_functions
import graph_functions
import numpy as np

def read_embeddings_file(filename):
	"""
	Function to read the embeddings file generated for the karate graph and stored in embeddings.txt
	"""
	rows = basic_functions.openCSVfile(filename)
	rows = rows[1:]
	vector_dict = {}
	for row in rows:
		r = row[0].split(" ")
		node = int(r[0]);vector_str = r[1:];vector = []
		for v in vector_str:
			vector.append(float(v))
		#print(node,vector,len(vector))
		vector_dict[node] = vector
	return vector_dict


def cosine_similarity(arr1,arr2):
	"""
	Cosine Similarity of arr1 and arr2
	"""
	cos = np.dot(arr1,arr2)
	v1 = np.sum(np.square(arr1))
	v2 = np.sum(np.square(arr2))
	return cos/(v1*v2)

#---------------------------Q2 a)---------------------------------
edge_list_path = "../data/karate.edgelist.txt"
G = nx.read_edgelist(edge_list_path, delimiter = " ", encoding='utf-8')
nx.draw(G, with_labels = True, pos = nx.spring_layout(G)) 
degrees = G.degree()
print("-------------------------Degrees of the Nodes----------------------")
print(degrees)
plt.show()



#---------------------------Q2 b)---------------------------------
# Reasoning written in report 

#---------------------------Q2 c)---------------------------------

#Declaring model hyper parameters
node2vec = Node2Vec(G,dimensions = 16,walk_length = 60,p = 0.01,q = 100,quiet = True,num_walks = 200, workers=4)  
#Node2Vec
model = node2vec.fit(window = 10, min_count = 1, batch_words = 4)
#Saving embedding file
model.wv.save_word2vec_format("Q2_c_embeddings.txt")
#Loading embedding file
vector_dict = read_embeddings_file("Q2_c_embeddings.txt")

#Embedding for Node 34
embed_34 = np.array(vector_dict[33])

#Dictionary for cosine similarity dictionary
cosine_sim_dict = {}

for v in vector_dict:
	if v != 33:
		embed = np.array(vector_dict[v])
		cos = cosine_similarity(embed_34,embed)
		cosine_sim_dict[v] = cos

#Sorting Cosine Dictionary
cosine_sim_dict = basic_functions.sortDictionary(cosine_sim_dict,attribute = "v",rev = True)

#Calculating Shortest Length#
shortest_path_length = nx.shortest_path_length(G,target = '33')

t = 0
for i in cosine_sim_dict:
	shortest_path = shortest_path_length[str(i)]
	cosine = cosine_sim_dict[i]
	print("Node = ",i,"shortest_path_length with node 33 = ",shortest_path,"Cosine Similarity with node 33 =",cosine)
	if t >= 4:
		break
	t += 1


#---------------------------Q2 d)---------------------------------

node2vec = Node2Vec(G,dimensions = 16,walk_length = 60,p = 100, q = 0.01,quiet = True,num_walks = 200, workers=4)  
model = node2vec.fit(window = 10, min_count = 1, batch_words = 4)
model.wv.save_word2vec_format("Q2_d_embeddings.txt")
vector_dict = read_embeddings_file("Q2_d_embeddings.txt")

#Embedding for Node 34
embed_34 = np.array(vector_dict[34])
#Cosine Similarity Dictionary with node 34
cosine_sim_dict = {}
#Making the dictionary
for v in vector_dict:
	if v != 34:
		embed = np.array(vector_dict[v])
		cos = cosine_similarity(embed_34,embed)
		cosine_sim_dict[v] = cos

#Cosine Similarity Dictionary
cosine_sim_dict = basic_functions.sortDictionary(cosine_sim_dict,attribute = "v",rev = True)

#Print 
t = 0
for i in cosine_sim_dict:
	degree = G.degree(str(i))
	cosine = cosine_sim_dict[i]
	print("Node = ",i,"Degree = ",degree,"Cosine Similarity with node 34 =",cosine)
	if t >= 4:
		break
	t += 1
#---------------------------Q2 e)---------------------------------

node2vec = Node2Vec(G,dimensions = 16,walk_length = 30,p = 100,q = 0.01,quiet = True,num_walks = 200, workers=4)  
model = node2vec.fit(window = 10, min_count=1, batch_words=4)  # Any keywords acceptable by gensim.Word2Vec can be passed, `diemnsions` and `workers` are automatically passed (from the Node2Vec constructor)
model.wv.save_word2vec_format("Q2_e_embeddings.txt")
vector_dict = read_embeddings_file("Q2_e_embeddings.txt")

#Minimum Eucledian Dictance Calculation
min_euclidean_dist = 100
min_euclidean_dist_v = None 
min_euclidean_dist_degree = None
node_33_degree = None 

#Embedding for node 33
embed_33 = np.array(vector_dict[33])

#Finding the simple minimum L2 norm euclidean distance via numpy
for v in vector_dict:
	if v != 33:
		embed = np.array(vector_dict[v])
		L2_norm = np.linalg.norm(embed_33-embed)
		#print(v,str(33),L2_norm)
		if min_euclidean_dist > L2_norm:
			min_euclidean_dist = L2_norm
			min_euclidean_dist_v = v


#Finding the node degree of the node  with min L2 Norm with 33 
for v_d in degrees:
	if int(v_d[0]) == min_euclidean_dist_v:
		min_euclidean_dist_degree = int(v_d[1])
	if int(v_d[0]) == 33:
		node_33_degree = int(v_d[1])
	

print("The minimum  Euclidean Distance is for vertex",min_euclidean_dist_v,"with a distance of",min_euclidean_dist,min_euclidean_dist_degree)
print("The degree for the node is for node 33 is ",node_33_degree)





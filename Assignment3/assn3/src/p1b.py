import networkx as nx
import basic_functions
import graph_functions
import matplotlib.pyplot as plt
import copy
import math

#The last digits of the node_id initially votes for
A_voted_by = [4,5,6,7]
B_voted_by = [0,1,2,3]
Undecided = [8,9]

#Changes the default global variable deciding an Undecided Candidate's votes
def change_Advantage(adv):
	adv = "A" if adv == "B" else "B"
	return adv

# Make a distribution of the dictionary
def make_distribution(dictionary):
	distribution = {}
	for v in dictionary:
		val = dictionary[v]
		if val in distribution:
			distribution[val].append(v) 
		else:
			distribution[val] = [v]
	return distribution

# Iniialize the votes
def votes_for(node_id,votes):
	vote = int(str(node_id)[-1])
	if vote in A_voted_by:
		votes[node_id] = "A"
	elif vote in B_voted_by:
		votes[node_id] = "B" 
	else:
		votes[node_id] = "U"
	return votes

#Make the group to whicthe advertisements are broadcasted for 
def make_Advertising_Group(amount):

	#The cost of assigning of each person is 1000/- pp 
	nfpeople_reached = amount//1000
	base_id = 3000
	advertised_to = []
	for i in range(nfpeople_reached):
		advertised_to.append(base_id + i)
	return advertised_to

#Change the voting patterns based on advertising
def advertise(group,votes,change_to):
	for person in group:
		votes[person] = change_to
	return votes

# Make the graph 
def make_graph(filename):
	G = nx.Graph()
	rows = basic_functions.openCSVfile(filename," ")
	Votes = {}
	for row in rows:
		node1_id = int(row[0])
		node2_id = int(row[1])
		G.add_edge(node1_id,node2_id)
		Votes = votes_for(node1_id,Votes)
		Votes = votes_for(node2_id,Votes)
	print(graph_functions.graphInfo(G,0,False,False,False))
	return G,Votes

#Determine the result of the election by counting the votes
def determine_result(final_votes):
	vote_distribution = make_distribution(final_votes)
	assert len(list(vote_distribution.keys())) == 2
	#print(vote_distribution.keys())
	nfVotesA = len(vote_distribution["A"])
	nfVotesB = len(vote_distribution["B"])

	if nfVotesA > nfVotesB:
		return "A",nfVotesA - nfVotesB
	elif nfVotesA < nfVotesB:
		return "B",nfVotesB - nfVotesA
	else:
		return "U",0

def simulate_election(G,nf_days,init_votes,advantage_candidate):
	#Make the distribution of votes
	dist_votes = make_distribution(init_votes)
	
	#Initial Undecided Voters
	init_undecided_voters = copy.deepcopy(dist_votes["U"])

	#Soritng the undecided Voters by voter_id
	init_undecided_voters.sort()
	
	current_votes = copy.deepcopy(init_votes)

	for iter_no in range(nf_days):

		for voter in init_undecided_voters:	
			
			# print("Undecided Voter = ",voter)

			nf_A_neighbor_voters = 0
			nf_B_neighbor_voters = 0
			nf_U_neighbor_voters = 0

			#Calculate the #Votes for each campaign and the undecided voters
			for neighbhor in G.neighbors(voter):

				if current_votes[neighbhor] == "A":
					nf_A_neighbor_voters += 1
				elif current_votes[neighbhor] == "B":
					nf_B_neighbor_voters += 1
				elif current_votes[neighbhor] == "U":
					nf_U_neighbor_voters += 1

			# Assign the final vote of the campaign
			if nf_A_neighbor_voters > nf_B_neighbor_voters:
				current_votes[voter] = "A"
			elif nf_A_neighbor_voters < nf_B_neighbor_voters:
				current_votes[voter] = "B"
			else:
				current_votes[voter] = advantage_candidate
				#print("Changing Advantage Candidate........")
				#print("Prev advantage_candidate = ",advantage_candidate)
				advantage_candidate = change_Advantage(advantage_candidate)
				#print("New advantage_candidate = ",advantage_candidate)

		#advantage_candidate = change_Advantage(advantage_candidate)

	return current_votes


def total_influence(G,advertising_group,initial_votes):
	vote_count = {"A": 0,"B": 0,"U":0}
	for node in advertising_group:
		for neighbor in G.neighbors(node):
			if initial_votes[neighbors] == "A":
				vote_count["A"] += 1


def advertise_before_simulate(G,amount,nf_days,init_votes,advantage_candidate,title = ""):
	margin_won = []
	amounts_spend = []
	min_margin = math.inf
	ideal_amount = math.inf

	for k in range(0,amount+1,1000):

		#Making the Advertising Group
		advertise_to = make_Advertising_Group(k)
		#Changing their votes permanently to "A"
		init_votes1 = advertise(advertise_to,init_votes,"A")

		#Simulating the election same as before
		final_votes = simulate_election(G,nf_days = 7,init_votes = init_votes1,advantage_candidate = advantage_candidate)
		winner,margin = determine_result(final_votes)

		
		#print("The election was won by",winner,"with a margin of",margin,"amount spend",k)

		# If "B" is the winner ,margin is -ve w.r.t A
		if winner == "B":
			margin =  -1 * margin
		
		if winner == "A":
			if margin < min_margin:
				min_margin = margin
				ideal_amount = k

		margin_won.append(margin)
		amounts_spend.append(k)

	#Making the plot  
	plt.plot(amounts_spend,margin_won)
	plt.xlabel("Amount Spend")
	plt.ylabel("Margin of Victory")
	plt.xticks([0,10000,20000,30000,40000,50000,60000,70000,80000,90000])
	plt.title(title)
	plt.show()

	return min_margin,ideal_amount



Adv_Candidate = "A"

G1,Init_Votes1 = make_graph("../q1-data/g1.edgelist.txt")
G2,Init_Votes2 = make_graph("../q1-data/g2.edgelist.txt")

print("------------------------------SOCIAL GRAPH 1-----------------------------------")
min_margin,ideal_amount = advertise_before_simulate(G1,amount = 90000,nf_days = 7,init_votes = Init_Votes1,advantage_candidate = Adv_Candidate,title = "G1 Social graph")
print("The minimum amount of money that needs to be spent by A is ",ideal_amount,"winning by",min_margin)
print("------------------------------SOCIAL GRAPH 2-----------------------------------")
min_margin,ideal_amount  = advertise_before_simulate(G2,amount = 90000,nf_days = 7,init_votes = Init_Votes2,advantage_candidate = Adv_Candidate,title = "G2 Social graph")
print("The minimum amount of money that needs to be spent by A is ",ideal_amount,"winning by",min_margin)




	





import json
import csv
import collections
import pickle
import os
import shutil




#-------------------------Pickle Functions-------------------------------------------------------
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

#-------------------------JSON Functions-------------------------------------------------------
def dumpJsonFile(dictionary,filepath):
	print("Dumping a dictionary to filepath",filepath,"...............")
	with open(filepath,"w+") as jsonFile:
		json.dump(dictionary,jsonFile,indent=4,sort_keys =True)
	print("Dumped Successfully")

def loadJsonFile(filepath):
	print("Loading a dictionary to filepath",filepath,"...............")
	dictionary = {}
	with open(filepath) as jsonFile:
		dictionary = json.load(jsonFile)
	print("Loaded Successfully")
	return dictionary


#-------------------------CSV Functions----------------------------------------------------------
def appendToCSV(row,filepath):
	with open(filepath,"a",buffering = 1) as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(row)

def openCSVfile(filepath,delimiter = ","):
	with open(filepath,"r") as csvfile:
		rows =  csv.reader(csvfile,delimiter = delimiter)
		return list(rows)

def csvTojson(csvfile,jsonfile):
	rows = []
	graph = {}
	with open(csvfile,"r") as csvfile:
		rows = csv.reader(csvfile)
		rows = list(rows)
	rows = rows[1:]
	print("Making graph....")
	for row in rows:
		source = row[0]
		target = row[1]
		weight = row[2]
		if source not in graph:
			graph[source] = {}
			graph[source][target] = int(weight)
		else:
			graph[source][target] = int(weight)
	print("Dumping to file.........")
	with open(jsonfile,"w") as jsonfile:
		json.dump(graph,jsonfile)
	print("Dumped json file")



#-------- Dictionrary Functions--------------------------------------------------------------
def revertDictionary(dictionary):
	newDictionary = {}
	print("")
	for key in dictionary.keys():
		value = dictionary[key]
		if value in dictionary:
			print("Cannot Revert Duplicate Values Present....")
			print("Returned the same dictionary as it is")
			return dictionary
		else:
			newDictionary[value] = key
	print("Successfully Reverted the dictionary")
	return newDictionary

def sortDictionary(dictionary,attribute = "k",rev = True):
	od = {}
	if attribute == "k":
		print("Ordering by key.....")
		od = collections.OrderedDict(sorted(dictionary.items(), key=lambda t: t[0],reverse = rev))  
	elif attribute == "v":
		print("Ordering by Value.....")
		od = collections.OrderedDict(sorted(dictionary.items(), key=lambda t: t[1],reverse = rev))
	else:
		print("Invalid attribute")
	return od


#------------------------OS FUNCTIONS----------------------------------------
def get_directory_list(folderpath):
    directory_list = []
    for root,d_names,f_names in os.walk(folderpath):
        for dname in d_names:
            if dname.find("2019") != -1:
                #print(dname)
                directory_list.append(dname)

    directory_list.sort()
    for d in directory_list:
        print(d)
    return directory_list

def get_file_list(folderpath):
    file_list = []
    for root,d_names,f_names in os.walk(folderpath):
        for fname in f_names:
            file_list.append(fname)
    file_list.sort()
    return file_list

#--------------------


def copy_file(filepath,copy_to_filepath):
	newPath = shutil.copy(filepath,copy_to_filepath)
	return newPath

if __name__ == "__main__":
	pass
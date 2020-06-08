import csv
import basic_functions
import graph_functions
import matplotlib.pyplot as plt

rows = basic_functions.openCSVfile("Q3_Loss_Accuracy.txt","|")
epochs = []
test_loss = []
test_accuracies = []

for row in rows:
	epoch_no = int(row[0].split(' ')[1])
	loss = float(row[1].split(' ')[2])
	test_accuracy = float(row[2].split(' ')[3])
	print(epoch_no,loss,test_accuracy)
	epochs.append(epoch_no + 1)
	test_loss.append(loss)
	test_accuracies.append(test_accuracy)


plt.plot(epochs,test_accuracies)
plt.xlabel("Epoch No")
plt.ylabel("Test Accuracy")
plt.show()

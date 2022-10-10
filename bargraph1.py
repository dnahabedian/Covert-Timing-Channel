import matplotlib.pyplot as plt
import csv

x = [] # store the csv vals
y = [] # calc the interpacket delay

with open("Traffic_data_orig.csv", "r") as csvfile:
    dataCSV = csv.reader(csvfile, delimiter = ",")
    temp = []

    for row in dataCSV:
        temp.append(row[1])
    
    temp.pop(0)     #remove Time from the list

    for i in range(len(temp)):
        x.append(float(temp[i]))

for i in range(0, (len(x) - 1)):
    a1 = x[i]
    a2 = x[i + 1]

    y.append(a2 - a1)

plt.hist(y)
plt.show()
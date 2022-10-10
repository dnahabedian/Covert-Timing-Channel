import matplotlib.pyplot as plt
import csv
import statistics
import random

random.seed(1237)

x = "this is a secret message"
count = 0
m, minVal, maxVal = 0.0, 0.0, 0.0

# Store the delanewDelays in newDelay, unmodDelay packet delanewDelay in unmodDelay
secretMess, modDelay, unmodDelay, timeBTW = [], [], [], []

for i in x:
    secretMess.append(bin(ord(i)).replace('b', ''))

with open("Traffic_data_orig.csv", "r") as csvfile:
    dataCSV = csv.reader(csvfile, delimiter=",")
    temp = []

    for row in dataCSV:
        temp.append(row[1])

    temp.pop(0)  # remove Time from the list

    for i in range(len(temp)):
        unmodDelay.append(float(temp[i]))

for i in range(0, (len(unmodDelay) - 1)):
    a1 = unmodDelay[i]
    a2 = unmodDelay[i + 1]

    timeBTW.append(a2 - a1)

m = statistics.median(timeBTW)
maxVal = max(timeBTW)
minVal = min(timeBTW)

while count < (len(secretMess)):
    for str in secretMess[count]:
        if str == "0":
            modDelay.append(random.uniform(m, minVal))
        else:
            modDelay.append(random.uniform(m, maxVal))
    count = count + 1

newDelay = modDelay + timeBTW
plt.hist(newDelay)
plt.show()

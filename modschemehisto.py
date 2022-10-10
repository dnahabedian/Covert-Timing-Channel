import matplotlib.pyplot as plt

x = "this is a secret message"
a = []
y = [] #store the delays of the message in here
count = 0

for i in x:
    a.append(bin(ord(i)).replace('b', ''))

while count < (len(a)):
    for str in a[count]:
        if str == "0":
            y.append(0.25)
        else:
            y.append(0.75)
    count = count + 1

plt.hist(y)
plt.show()
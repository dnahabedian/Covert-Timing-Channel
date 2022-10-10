x = "this is a secret message"

for i in x:
    a = bin(ord(i)).replace('b', '')
    print(a)

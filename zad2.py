x = [0, 3, 1, 2, 5, 4]
hood = []

for i in range(len(x)-1):
    for j in range(len(x)-1-i):
        hood.append([x[i], x[i + j+1]])

print(len(hood), hood)

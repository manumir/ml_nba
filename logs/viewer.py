with open('january_mlp.txt') as f:
	right,wrong=[],[]
	lines=f.readlines()
	for line in lines:
		if len(line)==37:
			right.append(line)
		else:
			wrong.append(line)

count=0
for line in right:
	count+=float(line[-5:-1])
print(count-len(wrong))

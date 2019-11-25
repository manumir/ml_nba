with open('gains_nba','r') as file:
	lines=file.readlines()
	count=0
	for line in lines:
		count=count+float(line)
count=round(count,2)
print(count)
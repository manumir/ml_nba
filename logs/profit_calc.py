import re

with open('gains_nba','r') as file:
	lines=file.readlines()
	count=0
	for line in lines:
		match=re.search('#',line)
		if match:
			count=count+float(line[:match.start()-1])
		else:
			count=count+float(line)
count=round(count,2)
print(count)
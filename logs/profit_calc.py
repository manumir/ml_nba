#! /usr/bin/python3

import re

with open('gains_nba','r') as file:
	lines=file.readlines()
	count=0
	count_january=0
	for line in lines:
		match=re.search('#',line)
		if match:
			count=count+float(line[:match.start()-1])
			count_january=count_january+float(line[:match.start()-1])
		else:
			count=count+float(line)
			count_january=count_january+float(line)
		
		if line=='0 # started by program\n':
			count_january=0
			
print('total:',round(count,2))
print('january total:',round(count_january,2))

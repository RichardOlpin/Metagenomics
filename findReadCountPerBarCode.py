import sys
import gzip
import re
from collections import defaultdict


#Test Data
'''
lines = ["@M04734:21:000000000-AYJRD:1:1101:12264:1796 2:N:0:TGTCGCAGATCT+TACACCGTTATG",
"@M04734:21:000000000-AYJRD:1:1101:12680:1887 2:N:0:CTACGACCATCT+TGATATCTTCTT",
"@M04734:21:000000000-AYJRD:1:1101:15538:1916 2:N:0:TTAGCGCTATCT+TCATCGAGTATG",
"@M04734:21:000000000-AYJRD:1:1101:13776:1938 2:N:0:CGTCATACATCT+TACACCGTTATG",
"@M04734:21:000000000-AYJRD:1:1101:18049:1938 2:N:0:TCATACGTATCT+CGTGAGTGTATG",
"@M04734:21:000000000-AYJRD:1:1101:18090:1938 2:N:0:CATCGTGAATCT+CGGCGTGTTATG",
"@M04734:21:000000000-AYJRD:1:1101:14151:1938 2:N:0:GAGCTCGAATCT+GGCTATCTTATG",
"@M04734:21:000000000-AYJRD:1:1101:14729:1938 2:N:0:TTTACAGCATCT+GACACCGTTATG",
"@M04734:21:000000000-AYJRD:1:1101:14672:1943 2:N:0:TTTTTTTTTTCT+TCTTTCCCTACA",
"@M04734:21:000000000-AYJRD:1:1101:16763:1948 2:N:0:CAGCTTGCATCT+ATCATCTGTATG",
"@M04734:21:000000000-AYJRD:1:1101:17777:1949 2:N:0:TCTTCATGATCT+TCTTTCTGTATG",
"@M04734:21:000000000-AYJRD:1:1101:13671:1950 2:N:0:TTAGCGCTATCT+GGATATCTTATG",
"@M04734:21:000000000-AYJRD:1:1101:18514:1958 2:N:0:TAGCTCGAATCT+ACTATCTGTATG"]
'''

unique8Combo = []
unique8Front = []
unique8Back = []

unique12Combo = []
unique12Front = []
unique12Back = []




def addBarcodesToSets(combo8,front8,back8,combo12,front12,back12):
	size8Combo = len(unique8Combo)
	size8Front = len(unique8Front)
	size8Back = len(unique8Back)
	
	size12Combo = len(unique12Combo)
	size12Front = len(unique12Front)
	size12Back = len(unique12Back)


	unique8Combo.append(combo8)
	unique8Front.append(front8)
	unique8Back.append(back8)
		
	unique12Combo.append(combo12)
	unique12Front.append(front12)
	unique12Back.append(back12)

	
	


with gzip.open(sys.argv[1],'rt') as  f:

	pat8 =re.compile("@\w\d+:\d+:\d+-\w+:\d:\d+:\d+:\d+\s\d:\w:\d:(\w{8})\w{4}\+(\w{8})")
	pat12 = re.compile("@\w\d+:\d+:\d+-\w+:\d:\d+:\d+:\d+\s\d:\w:\d:(\w{12})\+(\w{12})")

	i = 0

	for line in f:
		#print(line)
#		if i < 150000:
		if line[0] == '@' and len(line) < 80:
			i +=1
#			print(line.strip())	
			match8 = pat8.search(line)
			match12 = pat12.search(line)
		
			combo8 =  (match8.group(1) + '+' + match8.group(2))
			combo12 = (match12.group(1) + '+' + match12.group(2))
#			print(combo8)	
			front8 = match8.group(1)
			back8 = match8.group(2)
			
			front12 = match12.group(1)
			back12 = match12.group(2)
			
			addBarcodesToSets(combo8,front8,back8,combo12,front12,back12)
#		else:
#			break


	combo8D = defaultdict(int)
	front8D = defaultdict(int)
	back8D = defaultdict(int)

	combo12D = defaultdict(int)
	front12D = defaultdict(int)
	back12D = defaultdict(int)

	for j in unique8Combo:
		combo8D[j] +=1
	for j in unique8Front:
		front8D[j] +=1
	for j in unique8Back:
		back8D[j] +=1



	for j in unique12Combo:
		combo12D[j] +=1
	for j in unique12Front:
		front12D[j] +=1
	for j in unique8Back:
		back12D[j] +=1

	#Write separate files for each combo with the count for each 

	with open("combo8.txt",'w') as o:
		o.write("Combo8\tCount\n")
		for k,v in combo8D.items():
			combo8Out=str(k) +"\t"+str(v)+"\n"
			o.write(combo8Out)
		o.close()
	with open("front8.txt",'w') as o:
		o.write("front8\tCount\n")
		for k,v in front8D.items():
			combo8Out=str(k) +"\t"+str(v)+"\n"
			o.write(combo8Out)
		o.close()
	with open("back8.txt",'w') as o:
		o.write("back8\tCount\n")
		for k,v in back8D.items():
			combo8Out=str(k) +"\t"+str(v)+"\n"
			o.write(combo8Out)
		o.close()
	with open("combo12.txt",'w') as o:
		o.write("Combo12\tCount\n")
		for k,v in combo12D.items():
			combo8Out=str(k) +"\t"+str(v)+"\n"
			o.write(combo8Out)
	with open("front12.txt",'w') as o:
		o.write("front12\tCount\n")
		for k,v in front12D.items():
			combo8Out=str(k) +"\t"+str(v)+"\n"
			o.write(combo8Out)
		o.close()
	with open("back12.txt",'w') as o:
		o.write("back12\tCount\n")
		for k,v in back12D.items():
			combo8Out=str(k) +"\t"+str(v)+"\n"
			o.write(combo8Out)
		o.close()









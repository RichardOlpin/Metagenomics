import sys
import gzip
import re

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

unique8Combo = set()
unique8Front = set()
unique8Back = set()

unique12Combo = set()
unique12Front = set()
unique12Back = set()

combo8D = {}


#for line in lines:
#	pat8 =re.compile("@\w\d+:\d+:\d+-\w+:\d:\d+:\d+:\d+\s\d:\w:\d:(\w{12})\+(\w{12})")
#	match = re.search(pat8,line)
#	print (match.group(1) +' + '+match.group(2))


def addBarcodesToSets(combo8,front8,back8,combo12,front12,back12):
	size8Combo = len(unique8Combo)
	size8Front = len(unique8Front)
	size8Back = len(unique8Back)
	
	size12Combo = len(unique12Combo)
	size12Front = len(unique12Front)
	size12Back = len(unique12Back)


	unique8Combo.add(combo8)
	unique8Front.add(front8)
	unique8Back.add(back8)
		
	unique12Combo.add(combo12)
	unique12Front.add(front12)
	unique12Back.add(back12)

	# checking to see if there were any new barcodes
	#if (len(unique8Combo) > size8combo):
	



	#print(unique12Combo)
	
	


with gzip.open(sys.argv[1],'rt') as  f:

	pat8 =re.compile("@\w\d+:\d+:\d+-\w+:\d:\d+:\d+:\d+\s\d:\w:\d:(\w{8})\w{4}\+(\w{8})")
	pat12 = re.compile("@\w\d+:\d+:\d+-\w+:\d:\d+:\d+:\d+\s\d:\w:\d:(\w{12})\+(\w{12})")

	i = 0

	for line in f:
		#print(line)
#		if i < 500:
#			i+=1
		if line[0] == '@' and len(line) < 80:
				
			match8 = pat8.search(line)
			match12 = pat12.search(line)
		
			combo8 =  (match8.group(1) + '+' + match8.group(2))
			combo12 = (match12.group(1) + '+' + match12.group(2))
#				print(combo8)	
			front8 = match8.group(1)
			back8 = match8.group(2)
			
			front12 = match12.group(1)
			back12 = match12.group(2)
			
			addBarcodesToSets(combo8,front8,back8,combo12,front12,back12)
#		else:
#			break
	print(len(unique8Combo))
	print(len(unique8Front))
	print(len(unique8Back))
	
	print(len(unique12Combo))
	print(len(unique12Front))
	print(len(unique12Back))
			





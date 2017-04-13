import sys
from collections import defaultdict
import gzip
import re
import datetime

'''
Notes: Run this scipt in the output directory you desire.
		This is intended for the Doody_FlySeq data set as the bar code combinations are hard coded
'''



def parseBadFastq(headerList, readBlockDict, unmatchedReadsDict,Barcode_sampleIdDict,uniqueBarcodeSet):
	print("In parseBadFastq at: " + str(datetime.datetime.now()))
	Index1List = ["TACTAGGT", "ACGTACGT", "CGCGATAT", "CTATCGTG", "GCGATACG", "AGTCGCAG", "GTTACAGC", "TAACGTCC", "CTACGACC", "GAGACTTA", "ACTGTGTA", "TGCGTCAA", "AGCATACC", "CGTCATAC", "TCAGTCTA", "CATCGTGA", "GAGCTCGA", "ATAGCGCT", "TCTAGACT", "CAGTAGGT", "TCCTCATG" ,"CGAGCTAG" ,"CTCTAGAG", "ATGAGCTC"]
	
	Index2List = ["ATCGTACG", "ACTATCTG", "TAGCGAGT", "GGATATCT", "GACACCGT", "CTGCGTGT", "TCATCGAG", "CGTGAGTG"]


	ind1count = 0
	ind2count = 0
	matchedReadBlock = ""	# This will contain the header and the following 3 lines associated with that particular read
	allMatchedBlocksPerBarcode = ""		# This will contain all of the read blocks above for the current barcode
	numMatches = 0
	totalNumMatches = 0
	
	firstTimeThrough = 1		# First time through we will create a dict mapping a tag (read1,read2...) in order to a header line (@.......) 
#	unmatchedReadsDict =		# Dict, {key = read25, value = @header line}, at the end this will only contain reads that did not match any barcode combo
	matchedReadList = []		# This will have all the reads header lines number. read25 would be on line 100 in the original file (read# * 4) 
	readCounter = 0				# keep track of what read we are on, indexing with 1, increments before it writes
	barcodeCount = 0
	allSumStats = ""

	for barcode1 in Index1List:
		for barcode2 in Index2List:
			barcodeCount += 1
			#print("Checking with New barcode at : " + str(datetime.datetime.now()))
			del allMatchedBlocksPerBarcode
			allMatchedBlocksPerBarcode = ""
			matchedReadBlock = ""
			newTime = datetime.datetime.now()

			print("Checking new barcode " + str(barcodeCount)  + " of 192 at " + str(newTime))
			
			for header in headerList:
				header = header.strip()
				readCounter +=1
				part2 = r"\w{4}\+"
				#		Matches the header				Barcode1    extra tag+ barcode2
				pat = re.compile("@\w\d+:\d+:\d+-\w+:\d:\d+:\d+:\d+\s\d:\w:\d:"+re.escape(barcode1) + part2 + re.escape(barcode2) )
				
				if pat.search(header):		# looking for exact line matches "Idpart:Barcode1{4Letters}+Barcode2{4Letters}"		
					numMatches += 1
					totalNumMatches +=1
					matchedReadBlock = readBlockDict[header]		#Grab the header and following three lines which is the dict value			
					allMatchedBlocksPerBarcode += matchedReadBlock		#Concat all matched Read blocks into one object
					matchedReadBlock = ""					# wipe it, Im done with it
					matchedRead = str(readCounter)				#grab the read number
					matchedReadList.append(matchedRead)			#add it to the list of matched reads for this barcode
					readBlockDict.pop(header)				# remove this key and value because it has been matched to a combo
					unmatchedReadsDict.pop(readCounter)
			print("Found "+str(numMatches) + " For Barcode " + barcode1+ '+' +barcode2)	# Get some Screen output to let us know progress
			if allMatchedBlocksPerBarcode !="":			# only write a file if it finds matches. I know there are 50 barcodes that it will not find any matches
				# Writing all matched reads to New file for each barcode
				writeFastq(barcode1,barcode2,numMatches,matchedReadList,allMatchedBlocksPerBarcode,Barcode_sampleIdDict)
			
			
			#Writing a log file
			sumLine = createSumLine(barcode1,barcode2,numMatches,matchedReadList,Barcode_sampleIdDict)
			allSumStats += sumLine
			
			#Reset
			numMatches = 0
			matchedReadList[:] = []	# Delet all items in the list
			allMatchedBlocksPerBarcode = ""
			sumLine = ""
			readCounter =0


	writeUnmatchedReads(unmatchedReadsDict)	


	#print(len(readBlockDict))
	fh.close()
	headerListSize = len(headerList) 
	allSumStatsList = createSumStats(allSumStats,totalNumMatches,headerListSize)
	return allSumStatsList


def checkForUniqueBarcode(barcode1,barcode2,pat,uniqueBarcodeSet,headerList):
	barcode = barcode1 + "+" +barcode2
	prevSize = len(uniqueBarcodeSet)
	uniqueBarcodeSet.add(barcode)
	if len(uniqueBarcode) == prevSize:
		return 0
	else:
		return 1
	

def writeFastq(barcode1,barcode2,numMatches,matchedReadList,allMatchedBlocksPerBarcode,Barcode_sampleIdDict):
	print("Writing new fastq.gz at "+str(datetime.datetime.now()))
	barcode = barcode1+barcode2
	if barcode in Barcode_sampleIdDict:
		fileName = Barcode_sampleIdDict[barcode]
	else:
		fileName = barcode1 + "+" + barcode2
	with gzip.open(str(fileName) + ".fastq.gz", 'a') as output:        #write gzip file to save space
		line1 = "#Matched " + str(numMatches) + " Reads to Barcode Combo: " + str(barcode1) + " + " + str(barcode2) + "\n"
		line1bytes = str.encode(line1)
		line2 = "#All Matched Reads:" + ','.join(matchedReadList)+"\n"
		line2bytes = str.encode(line2)
		output.write(line1bytes)
		output.write(line2bytes)
		
		blocks = str.encode(allMatchedBlocksPerBarcode)
		output.write(blocks)
	output.close()	



def writeUnmatchedReads(unmatchedReadsDict):
	#Write summary .txt file
	with open("unmatchedReads.txt",'w') as o:
		o.write("Read#\tHeaderLine\n")
		for key,value in unmatchedReadsDict.items():
			o.write(str(key) +"\t"+value +"\n")
	o.close()
	
	#write fastq.gz file for further analysis
	with gzip.open("UnmatchedReads.fastq.gz",'w') as o2:
		for key,value in unmatchedReadsDict.items():
			valueBytes = str.encode(value)	
			o2.write(valueBytes)
	o2.close()
	


def createSumStats(allSumStats,totalNumMatches,headerListSize):
	logHeaderLine = "Barcode\tNumMatchedReads\tReads (#*4)\n"
	logTxt = ""
	logTxt = createallSumStatsTxt(allSumStats,totalNumMatches,headerListSize,logHeaderLine)
	logCsv = createallSumStatsCsv(allSumStats,logHeaderLine)
	allSumStatsList = [logTxt,logCsv]
	return allSumStatsList



def createallSumStatsTxt(allSumStats,totalNumMatches,headerListSize,logHeaderLine):
	numMatchesLine = "#Total Number of Matches = " + str(totalNumMatches) + " out of " + str(headerListSize) + "\n"	
	logTxt = ""
	logTxt += numMatchesLine + logHeaderLine + allSumStats
	
	return logTxt

def createallSumStatsCsv(allSumStats,logHeaderLine):
	return( logHeaderLine + allSumStats)
	


def createSumLine(barcode1,barcode2,numMatches,matchedReadList,Barcode_sampleIdDict):
	name = ""
	barcode = barcode1+barcode2
	if barcode in Barcode_sampleIdDict:
		name = Barcode_sampleIdDict[barcode]
	else:
		name = (barcode1 + '+' + barcode2)
	if numMatches == 0:
		sumLine = (name+ "\t0\tNULL\n")
	else:
		sumLine = (name + "\t"+ str(numMatches) + "\t" + ','.join(matchedReadList)+"\n")
	return sumLine


def writeLogFile(allSumStats,timeResult):
	#print("Writing Log file at " + str(datetime.datetime.now())
	with open("log.txt",'w') as out:
		out.write(timeResult)
	#	out.write("Barcode\tNumMatchedReads\tReads (#*4)\n")
		out.write(allSumStats[0])
	out.close()

	with open("log.csv",'w') as out:
	#	out.write("Barcode\tNumMatchedReads\tReads (#*4)\n")
		out.write(allSumStats[1])
	out.close()

def createListAndDict(headerList, readBlockDict):
	i = 0
	print("Creating List and Dictionary at " + str(datetime.datetime.now()))
	for line in fh:
	#	if i <500: 
		if line[0] == "@":
			i+=1
			unmatchedReadsDict[i] = line.strip()
			headerList.append(line.strip())
			readBlock = line + next(fh)+ next(fh) + next(fh)
			readBlockDict[line.strip()] = readBlock
			readBlock = ""
	#	else:
	#		break	
	print("Number of Reads in File: " + str(i))
#	print(readBlockDict["@M04734:21:000000000-AYJRD:1:1101:18354:1928 2:N:0:CAGTAGGTATCT+GGATATCTTATG"])
#	for j in headerList:
#		print(j)

#	print("\n\n\n")
#	for k,v in readBlockDict.items():
#		print(k+"\t"+v+ "\n")


def createSampleID_BarcodeDict():
	barcodes = ["TACTAGGTATCGTACG", "ACGTACGTATCGTACG", "CGCGATATATCGTACG", "CTATCGTGATCGTACG", "GCGATACGATCGTACG", "AGTCGCAGATCGTACG", "GTTACAGCATCGTACG", "TAACGTCCATCGTACG",
"CTACGACCATCGTACG", "GAGACTTAATCGTACG", "ACTGTGTAATCGTACG", "TACTAGGTACTATCTG", "TGCGTCAAATCGTACG", "ACGTACGTACTATCTG", "CGCGATATACTATCTG", "CTATCGTGACTATCTG",
"GCGATACGACTATCTG", "AGTCGCAGACTATCTG", "GTTACAGCACTATCTG", "TAACGTCCACTATCTG", "CTACGACCACTATCTG", "GAGACTTAACTATCTG", "ACTGTGTAACTATCTG", "TGCGTCAAACTATCTG",
"TACTAGGTTAGCGAGT", "ACGTACGTTAGCGAGT", "CGCGATATTAGCGAGT", "CTATCGTGTAGCGAGT", "GCGATACGTAGCGAGT", "AGTCGCAGTAGCGAGT", "GTTACAGCTAGCGAGT", "TAACGTCCTAGCGAGT",
"TACTAGGTGGATATCT", "AGCATACCGACACCGT", "ACGTACGTGGATATCT", "CGTCATACGACACCGT", "CGCGATATGGATATCT", "TCAGTCTAGACACCGT", "CTATCGTGGGATATCT", "CATCGTGAGACACCGT",
"GCGATACGGGATATCT", "GAGCTCGAGACACCGT", "ATAGCGCTGACACCGT", "TCTAGACTGACACCGT", "CAGTAGGTATCGTACG", "ATAGCGCTATCGTACG", "TCTAGACTATCGTACG", "TCCTCATGATCGTACG",
"CGAGCTAGATCGTACG", "CTCTAGAGATCGTACG", "ATGAGCTCATCGTACG", "AGCATACCATCGTACG", "CGTCATACATCGTACG", "TCAGTCTAATCGTACG", "CATCGTGAATCGTACG", "GAGCTCGAATCGTACG",
"CAGTAGGTACTATCTG", "CTCTAGAGGACACCGT", "ATAGCGCTACTATCTG", "TCTAGACTACTATCTG", "TCCTCATGACTATCTG", "CGAGCTAGACTATCTG", "CTCTAGAGACTATCTG", "ATGAGCTCACTATCTG",
"AGCATACCACTATCTG", "CGTCATACACTATCTG", "TCAGTCTAACTATCTG", "CATCGTGAACTATCTG", "GAGCTCGAACTATCTG", "CAGTAGGTTAGCGAGT", "ATAGCGCTTAGCGAGT", "TCTAGACTTAGCGAGT",
"TCCTCATGTAGCGAGT", "CGAGCTAGTAGCGAGT", "CTCTAGAGTAGCGAGT", "ATGAGCTCTAGCGAGT", "ATGAGCTCGACACCGT", "AGCATACCTAGCGAGT", "AGTCGCAGGGATATCT", "CGTCATACTAGCGAGT",
"GTTACAGCGGATATCT", "TCAGTCTATAGCGAGT", "TAACGTCCGGATATCT", "CATCGTGATAGCGAGT", "CTACGACCGGATATCT", "GAGCTCGATAGCGAGT", "GAGACTTAGGATATCT", "CAGTAGGTGGATATCT",
"TCCTCATGGACACCGT", "CAGTAGGTCTGCGTGT", "ATAGCGCTCTGCGTGT", "TCTAGACTCTGCGTGT", "TCCTCATGCTGCGTGT", "CGAGCTAGCTGCGTGT", "CTCTAGAGCTGCGTGT", "ATGAGCTCCTGCGTGT",
"AGCATACCCTGCGTGT", "CGTCATACCTGCGTGT", "TCAGTCTACTGCGTGT", "CATCGTGACTGCGTGT", "GAGCTCGACTGCGTGT", "CAGTAGGTTCATCGAG", "ATAGCGCTTCATCGAG", "TCTAGACTTCATCGAG",
"TCCTCATGTCATCGAG", "CGAGCTAGTCATCGAG", "CTCTAGAGTCATCGAG", "ATGAGCTCTCATCGAG", "AGCATACCTCATCGAG", "CGTCATACTCATCGAG", "TCAGTCTATCATCGAG", "CATCGTGATCATCGAG",
"GAGCTCGATCATCGAG", "CAGTAGGTCGTGAGTG", "ATAGCGCTCGTGAGTG", "TCTAGACTCGTGAGTG", "TCCTCATGCGTGAGTG", "CGAGCTAGCGTGAGTG", "CTCTAGAGCGTGAGTG", "ATGAGCTCCGTGAGTG",
"AGCATACCCGTGAGTG", "TACTAGGTGACACCGT", "CGTCATACCGTGAGTG", "ACGTACGTGACACCGT", "TCAGTCTACGTGAGTG", "CGCGATATGACACCGT", "CATCGTGACGTGAGTG", "CTATCGTGGACACCGT",
"GAGCTCGACGTGAGTG", "GCGATACGGACACCGT", "CAGTAGGTGACACCGT", "CGAGCTAGGACACCGT", "ATAGCGCTGGATATCT", "TCTAGACTGGATATCT", "TCCTCATGGGATATCT", "CGAGCTAGGGATATCT",
"CTCTAGAGGGATATCT", "ATGAGCTCGGATATCT", "AGCATACCGGATATCT", "CGTCATACGGATATCT", "CATCGTGAGGATATCT", "GAGCTCGAGGATATCT"]

	sampleIDs = ['1.00', '1.01', '1.02', '1.03', '1.04', '1.05', '1.06', '1.07', '1.08', '1.09', '1.10', '1.11', '1.12', '1.13', '1.14', '1.15', '1.16', '1.17', '1.18', '1.19', '1.20', '1.21', '1.22', '1.23', '1.24', '1.25', '1.26', '1.27', '1.28', '1.29', '1.30', '1.31', '1.32', '1.32', '1.33', '1.33', '1.34', '1.34', '1.35', '1.35', '1.36', '1.36', '1.37', '1.38', '2.00', '2.01', '2.02', '2.03', '2.04', '2.05', '2.06', '2.07', '2.08', '2.09', '2.10', '2.11', '2.12', '2.12', '2.13', '2.14', '2.15', '2.16', '2.17', '2.18', '2.19', '2.20', '2.21', '2.22', '2.23', '2.24', '2.25', '2.26', '2.27', '2.28', '2.29', '2.30', '2.31', '2.31', '2.32', '2.32', '2.33', '2.33', '2.34', '2.34', '2.35', '2.35', '2.36', '2.36', '2.37', '3.00', '3.01', '3.02', '3.03', '3.04', '3.05', '3.06', '3.07', '3.08', '3.09', '3.10', '3.11', '3.12', '3.13', '3.14', '3.15', '3.16', '3.17', '3.18', '3.19', '3.20', '3.21', '3.22', '3.23', '3.24', '3.25', '3.26', '3.27', '3.28', '3.29', '3.30', '3.31', '3.32', '3.32', '3.33', '3.33', '3.34', '3.34', '3.35', '3.35', '3.36', '3.36', '3.37', '4.00', '4.02', '4.04', '4.05', '4.06', '4.11', '4.12', '4.23', '4.29', '4.34']
	Barcode_sampleIdDict = defaultdict(list)
	barcodes_and_sampleIDS = zip(barcodes,sampleIDs)
	for barcode, sampleID in barcodes_and_sampleIDS:
		Barcode_sampleIdDict[barcode] = sampleID
	return Barcode_sampleIdDict

def read(headerList):
	print("Starting to read through array at "+str(datetime.datetime.now()))
	count = 0
	for i in headerList:
		count += 1
	print(count)

with gzip.open(sys.argv[1],'rt') as fh:
	startTime = datetime.datetime.now()
	print("Starting at: " + str(startTime))
	

	headerList = []		# all headers stored as strings

	readBlockDict = {}	# key = header line, value = read block (header + next three lines)
	unmatchedReadsDict = {} # key = read#, val = header line
	uniqueBarcodeSet = set()
		
	print("Starting at: " + str(startTime))
	createListAndDict(headerList,readBlockDict)	
	#read(headerList)
	Barcode_sampleIdDict = createSampleID_BarcodeDict()
	logFileReport = parseBadFastq(headerList,readBlockDict,unmatchedReadsDict,Barcode_sampleIdDict,uniqueBarcodeSet)	#returns info for log file in a long string			
	
		

	endTime = datetime.datetime.now()
	print("Ended at : " + str(endTime))
	totalRunTime = endTime - startTime
	print("Total Run Time = " + str(totalRunTime))
	timeResult= "#Started at: " + str(startTime) + ", Ended at: " + str(endTime) +"\n#Total Run time: "+ str(totalRunTime) +"\n"
	
	writeLogFile(logFileReport,timeResult)
	




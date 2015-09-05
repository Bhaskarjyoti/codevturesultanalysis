# this code is last updated with a fix on 28/08 ( what will happen if the result has only <8 subjects ). To avoid that code brekage, we have to keep a counter 
#This code is last modified and tested on 27/08 night 

# 23/08 /2015: WE ARE MODIFYING THE CODE FOR B TECH RESULTS >> Similar logic but it has to be modified

#this is the latest Code  20/08 EVENING ( why subject 2 and 3 are getting mixed up ) ... test with a single file 
# main functionality added: instead of subject 1,2,3 etc scs21 etc are now defining Mongo Subdocument 
# without that feature, it is impossible to handle different subject set scenarios

# Issues in getting data out of HTML (it is too much of hacking as HTML is FrontPage generated  code.. no class tag in the HTML)
#(a) Some result sheets are blank .. put that check in 
#(b) Some result sheets (for cases who has cleared backs) there are two sets of result .. neglect the 2nd one for the result fiel
#(c) For the above issues, picking up the total is not possible as that field is sometimes getting used by something else 
#(d) For some subject 2 and subject 3 are different .. So, we need a routine where we build the valueList and then finally arrange it as per our own list

# This CODE EXTRACTS INFORMATION FROM HTML FILE AND THEN INSERTS A DOCUMENT INTO MONGODB WITH THAT INFORMATION
# trying to extract the following information from the result.html 
# name, USN, Semester x, Result, 
# It also has to get 7 sets (Subject, External, Internal, Total,Result)


from BeautifulSoup import BeautifulSoup
import urllib2
import pprint
import pymongo
import csv
import os
from pymongo import MongoClient


# ==========================================================
#printing the vlaues in the document for checking

def check_value(valueList):
	print (".......inside check_value(valueList).........................")
	#print ("Print the b tags and pick up the first few (not the Pass P..)")	
	
	#print nameusn  #Semester
	#print semesternum  #semester no
	#print result    #Result : xxxxx
	 
	
	print (".....................................")
	print ("Printing the rows in the table..")
	print (".....................................")
	

	print valueList[0][0]  #semester
	print valueList[0][1]  #semester number 
	#print valueList[0][2]
	
	print valueList[1][0] #subject
	print valueList[1][1] #internal 
	print valueList[1][2] #external 
	print valueList[1][3] #total
	
	print valueList[2][0]  #sub1
	print valueList[2][1]  #Sub1Int
	print valueList[2][2]  #sub1Ext
	print valueList[2][3]  #sub1Tot
	
	print valueList[3][0] #sub2
	print valueList[3][1] #Sub2Int
	print valueList[3][2] #sub2Ext
	print valueList[3][3]  #sub2Tot
	
	print valueList[4][0]
	print valueList[4][1]
	print valueList[4][2]
	print valueList[4][3]
	
	print valueList[5][0]
	print valueList[5][1]
	print valueList[5][2]
	print valueList[5][3]

	print valueList[6][0]
	print valueList[6][1]
	print valueList[6][2]
	print valueList[6][3]

	print valueList[7][0]
	print valueList[7][1]
	print valueList[7][2]
	print valueList[7][3]

	print valueList[8][0]
	print valueList[8][1]
	print valueList[8][2]
	print valueList[8][3]

	print valueList[9][0]
	print valueList[9][1]
	print valueList[9][2]  
	print valueList[9][3]  

	#Total  .. dropping as this will be different for people who cleared back
	#Totalmarks
#=============================================================



# using local file create soup. You may have to modify this 
# for reading all files in the directory and for file name starting with college code

def process_file_updatedb(fname):
	with open(fname,"r") as foo_file:
		soup = BeautifulSoup(foo_file)  #soup is the full HTML
	
	
	#-----------------------------------------
	
	valueList = []  # this is a list of lists 
	blank=0 #flag of blank resultsheet 
	
	#--------------------------------------------
	tables = soup.findChildren('table')
	my_table=tables[11]  # we are targetting the 11th table in soup 
	
	#-------------------------------------
	# This is a special code to avoid some few results which has only two subjects 
	# logically now, we sHOULD not have blank result file as per current logic
	
	bolds= my_table.findAll('b')
	boldlen=len(bolds)
	if (boldlen>1):
		nameusn= bolds[0].string  #name and USN
		print "nameusn%s"%nameusn
	else:
		result = "resultsheet blank"
		blank=1	
	if (boldlen>2):
		semesternum= bolds[1].string + bolds[2].string
		print "semesternum%s"%semesternum
		if int(semesternum[-1]) != 6:  # THIS CHECK HAS TO BE MODIFIED for each semester 
			# There are stray cases where the student is only writing 1st semester backlog and the result sheet has only those results..program will break 
			blank=1
	if (boldlen>4):	
		result = bolds[3].string.replace('&nbsp;',' ')
	
	
	#print"Debug:result of this candidate after accessing bold elements...%s"%(result)  # will give an error unless assigned
	#---collect the subject pass/fail also -only when those fields are there------------
	#---unless you put these checks, it will bomb for few which has a different format -----------------
	
	if (boldlen>5):
		sub1res = bolds[4].string.replace('&nbsp;',' ')
		print sub1res
	if (boldlen>6):
		sub2res = bolds[5].string.replace('&nbsp;',' ')
		print sub2res
	if (boldlen>7):
		sub3res = bolds[6].string.replace('&nbsp;',' ')
		print sub3res
	if (boldlen>8):
		sub4res = bolds[7].string.replace('&nbsp;',' ')
		print sub4res
	if (boldlen>9):
		sub5res = bolds[8].string.replace('&nbsp;',' ')
		print sub5res
	if (boldlen>10):
		sub6res = bolds[9].string.replace('&nbsp;',' ')
		print sub6res
	if (boldlen>11):
		sub7res = bolds[10].string.replace('&nbsp;',' ')
		print sub7res
	#since B tech Semester 2 has 8 subjects 
	if (boldlen>12):
		sub8res = bolds[11].string.replace('&nbsp;',' ')
		print sub8res		
	#print "DBG: Here I am extracting each row of data for another student ..."
	valueList =[]	


	for row in soup.find("td", {"width" : "513"}).findAll('tr'):
		tds = row('td')  # here I am printing all the cells in a row (list of cells) and I need to extract them 
		 
		listInternal=[]
		#print tds[0].text.replace('&nbsp;',' ')
		listInternal.append(tds[0].text.replace('&nbsp;',' '))
		 
		#print tds[1].text.replace('&nbsp;',' ')
		listInternal.append(tds[1].text.replace('&nbsp;',' '))
		 
		#print tds[2].text.replace('&nbsp;',' ')
		listInternal.append(tds[2].text.replace('&nbsp;',' '))
		
		#print tds[3].text.replace('&nbsp;',' ')
		listInternal.append(tds[3].text.replace('&nbsp;',' '))
		valueList.append(listInternal)
	print "..........valueList before allocating sub1 etc..........................."	
	
		
	sizeOfVlist=len(valueList)  # this is a list of lists
	print "size of valueList %s" %(sizeOfVlist)
	if sizeOfVlist ==0 :
		blank=1
		print "blank result with size of valueList 0"
	
	if (sizeOfVlist>9):  #Otherwise this code will fail for candidates where blank result is there
		print valueList[2][0]
		print valueList[3][0]
		print valueList[4][0]
		print valueList[5][0]
		print valueList[6][0]
		print valueList[7][0]
		print valueList[8][0]
		print valueList[9][0]
		
	
	#Since the subject list itself varies from college to college, I have to
	# define the subject dynamically 
	# the code sucks .. once it works, we have to improve this !!
	
	found=0  # no of subjects found 
	
	if (blank==0):
		
		if (sizeOfVlist >2):

			if '10AL61' in valueList[2][0]:
				sub1="10AL61"
				found +=1
			elif '10CS62' in valueList[2][0]:
				sub1="10CS62"
				found +=1
			elif '10CS63' in valueList[2][0]:
				sub1="10CS63"
				found +=1
			elif '10CS64' in valueList[2][0]:
				sub1="10CS64"
				found +=1
			elif '10CS65' in valueList[2][0]:
				sub1="10CS65"
				found +=1
			elif '10CSL67' in valueList[2][0]:
				sub1="10CSL67"
				found +=1
			elif '10CSL68' in valueList[2][0]:
				sub1="10CSL68"
				found +=1
			elif '10CS661' in valueList[2][0]:
				sub1="10CS661"
				found +=1
			elif '10CS662' in valueList[2][0]:
				sub1="10CS662"
				found +=1
			elif '10CS663' in valueList[2][0]:
				sub1="10CS663"
				found +=1
			elif '10CS664' in valueList[2][0]:
				sub1="10CS664"
				found +=1
			elif '10CS665' in valueList[2][0]:
				sub1="10CS665"
				found +=1
			elif '10CS666' in valueList[2][0]:
				sub1="10CS666"
				found +=1
			
		
#for the 2nd subject 
		if (sizeOfVlist >3):
			
			if '10AL61' in valueList[3][0]:
				sub2="10AL61"
				found +=1
			elif '10CS62' in valueList[3][0]:
				sub2="10CS62"
				found +=1
			elif '10CS63' in valueList[3][0]:
				sub2="10CS63"
				found +=1
			elif '10CS64' in valueList[3][0]:
				sub2="10CS64"
				found +=1
			elif '10CS65' in valueList[3][0]:
				sub2="10CS65"
				found +=1
			elif '10CSL67' in valueList[3][0]:
				sub2="10CSL67"
				found +=1
			elif '10CSL68' in valueList[3][0]:
				sub2="10CSL68"
				found +=1
			elif '10CS661' in valueList[3][0]:
				sub2="10CS661"
				found +=1
			elif '10CS662' in valueList[3][0]:
				sub2="10CS662"
				found +=1
			elif '10CS663' in valueList[3][0]:
				sub2="10CS663"
				found +=1
			elif '10CS664' in valueList[3][0]:
				sub2="10CS664"
				found +=1
			elif '10CS665' in valueList[3][0]:
				sub2="10CS665"
				found +=1
			elif '10CS666' in valueList[3][0]:
				sub2="10CS666"
				found +=1

		
#for the 3rd subject 
		if (sizeOfVlist >4):
			
			if '10AL61' in valueList[4][0]:
				sub3="10AL61"
				found +=1
			elif '10CS62' in valueList[4][0]:
				sub3="10CS62"
				found +=1
			elif '10CS63' in valueList[4][0]:
				sub3="10CS63"
				found +=1
			elif '10CS64' in valueList[4][0]:
				sub3="10CS64"
				found +=1
			elif '10CS65' in valueList[4][0]:
				sub3="10CS65"
				found +=1
			elif '10CSL67' in valueList[4][0]:
				sub3="10CSL67"
				found +=1
			elif '10CSL68' in valueList[4][0]:
				sub3="10CSL68"
				found +=1
			elif '10CS661' in valueList[4][0]:
				sub3="10CS661"
				found +=1
			elif '10CS662' in valueList[4][0]:
				sub3="10CS662"
				found +=1
			elif '10CS663' in valueList[4][0]:
				sub3="10CS663"
				found +=1
			elif '10CS664' in valueList[4][0]:
				sub3="10CS664"
				found +=1
			elif '10CS665' in valueList[4][0]:
				sub3="10CS665"
				found +=1
			elif '10CS666' in valueList[4][0]:
				sub3="10CS666"
				found +=1

		
#for the 4th subject 
		if (sizeOfVlist>5):
			
			
			if '10AL61' in valueList[5][0]:
				sub4="10AL61"
				found +=1
			elif '10CS62' in valueList[5][0]:
				sub4="10CS62"
				found +=1
			elif '10CS63' in valueList[5][0]:
				sub4="10CS63"
				found +=1
			elif '10CS64' in valueList[5][0]:
				sub4="10CS64"
				found +=1
			elif '10CS65' in valueList[5][0]:
				sub4="10CS65"
				found +=1
			elif '10CSL67' in valueList[5][0]:
				sub4="10CSL67"
				found +=1
			elif '10CSL68' in valueList[5][0]:
				sub4="10CSL68"
				found +=1
			elif '10CS661' in valueList[5][0]:
				sub4="10CS661"
				found +=1
			elif '10CS662' in valueList[5][0]:
				sub4="10CS662"
				found +=1
			elif '10CS663' in valueList[5][0]:
				sub4="10CS663"
				found +=1
			elif '10CS664' in valueList[5][0]:
				sub4="10CS664"
				found +=1
			elif '10CS665' in valueList[5][0]:
				sub4="10CS665"
				found +=1
			elif '10CS666' in valueList[5][0]:
				sub4="10CS666"
				found +=1

		
#for the 5th subject 
		if (sizeOfVlist>6):
				
			if '10AL61' in valueList[6][0]:
				sub5="10AL61"
				found +=1
			elif '10CS62' in valueList[6][0]:
				sub5="10CS62"
				found +=1
			elif '10CS63' in valueList[6][0]:
				sub5="10CS63"
				found +=1
			elif '10CS64' in valueList[6][0]:
				sub5="10CS64"
				found +=1
			elif '10CS65' in valueList[6][0]:
				sub5="10CS65"
				found +=1
			elif '10CSL67' in valueList[6][0]:
				sub5="10CSL67"
				found +=1
			elif '10CSL68' in valueList[6][0]:
				sub5="10CSL68"
				found +=1
			elif '10CS661' in valueList[6][0]:
				sub5="10CS661"
				found +=1
			elif '10CS662' in valueList[6][0]:
				sub5="10CS662"
				found +=1
			elif '10CS663' in valueList[6][0]:
				sub5="10CS663"
				found +=1
			elif '10CS664' in valueList[6][0]:
				sub5="10CS664"
				found +=1
			elif '10CS665' in valueList[6][0]:
				sub5="10CS665"
				found +=1
			elif '10CS666' in valueList[6][0]:
				sub5="10CS666"
				found +=1

		
#for the 6th subject 
		if (sizeOfVlist > 7):
				
			if '10AL61' in valueList[7][0]:
				sub6="10AL61"
				found +=1
			elif '10CS62' in valueList[7][0]:
				sub6="10CS62"
				found +=1
			elif '10CS63' in valueList[7][0]:
				sub6="10CS63"
				found +=1
			elif '10CS64' in valueList[7][0]:
				sub6="10CS64"
				found +=1
			elif '10CS65' in valueList[7][0]:
				sub6="10CS65"
				found +=1
			elif '10CSL67' in valueList[7][0]:
				sub6="10CSL67"
				found +=1
			elif '10CSL68' in valueList[7][0]:
				sub6="10CSL68"
				found +=1
			elif '10CS661' in valueList[7][0]:
				sub6="10CS661"
				found +=1
			elif '10CS662' in valueList[7][0]:
				sub6="10CS662"
				found +=1
			elif '10CS663' in valueList[7][0]:
				sub6="10CS663"
				found +=1
			elif '10CS664' in valueList[7][0]:
				sub6="10CS664"
				found +=1
			elif '10CS665' in valueList[7][0]:
				sub6="10CS665"
				found +=1
			elif '10CS666' in valueList[7][0]:
				sub6="10CS666"
				found +=1

		
#for the 7th subject 
		if (sizeOfVlist >8):
				
			if '10AL61' in valueList[8][0]:
				sub7="10AL61"
				found +=1
			elif '10CS62' in valueList[8][0]:
				sub7="10CS62"
				found +=1
			elif '10CS63' in valueList[8][0]:
				sub7="10CS63"
				found +=1
			elif '10CS64' in valueList[8][0]:
				sub7="10CS64"
				found +=1
			elif '10CS65' in valueList[8][0]:
				sub7="10CS65"
				found +=1
			elif '10CSL67' in valueList[8][0]:
				sub7="10CSL67"
				found +=1
			elif '10CSL68' in valueList[8][0]:
				sub7="10CSL68"
				found +=1
			elif '10CS661' in valueList[8][0]:
				sub7="10CS661"
				found +=1
			elif '10CS662' in valueList[8][0]:
				sub7="10CS662"
				found +=1
			elif '10CS663' in valueList[8][0]:
				sub7="10CS663"
				found +=1
			elif '10CS664' in valueList[8][0]:
				sub7="10CS664"
				found +=1
			elif '10CS665' in valueList[8][0]:
				sub7="10CS665"
				found +=1
			elif '10CS666' in valueList[8][0]:
				sub7="10CS666"
				found +=1
				

#for the 8th subject 
		if (sizeOfVlist >9):
				
			if '10AL61' in valueList[9][0]:
				sub8="10AL61"
				found +=1
			elif '10CS62' in valueList[9][0]:
				sub8="10CS62"
				found +=1
			elif '10CS63' in valueList[9][0]:
				sub8="10CS63"
				found +=1
			elif '10CS64' in valueList[9][0]:
				sub8="10CS64"
				found +=1
			elif '10CS65' in valueList[9][0]:
				sub8="10CS65"
				found +=1
			elif '10CSL67' in valueList[9][0]:
				sub8="10CSL67"
				found +=1
			elif '10CSL68' in valueList[9][0]:
				sub8="10CSL68"
				found +=1
			elif '10CS661' in valueList[9][0]:
				sub8="10CS661"
				found +=1
			elif '10CS662' in valueList[9][0]:
				sub8="10CS662"
				found +=1
			elif '10CS663' in valueList[9][0]:
				sub8="10CS663"
				found +=1
			elif '10CS664' in valueList[9][0]:
				sub8="10CS664"
				found +=1
			elif '10CS665' in valueList[9][0]:
				sub8="10CS665"
				found +=1
			elif '10CS666' in valueList[9][0]:
				sub8="10CS666"
				found +=1
		
	#check_value(valueList)
		
	#================================================================
	
	# create a document and insert
	# we have to write code to get the college number 
	if (blank ==0):
		
		collegeCode=fname[0:3]
		
		print "college code: %s"%(collegeCode)
		#print college.items()
		
		collegeName=college[collegeCode]
		
		# uncomment below lines to test for one file  
		#collegeCode="1RG"
		#collegeName="Rajiv Gandhi Institute of Technology"
		
		
		
		sizeofVlist=len(valueList)
		print "size of valueList %s after allocating sub1,sub2 etc." %(sizeofVlist)
		
		print "blank flag signifying blank record or WRONG SEMESTER  = %s"%blank
		
		print "No of subjects found in the result for this semester : %s"%found
	
	if blank ==0 and sizeofVlist>9 :  # neglecting few cases where all 8 subjects are NOT printed ( it should never happen that way)
		
		if (found==8):
	
			post = {"college": {"collegeName": collegeName, "collegeCode":collegeCode},
				"student":{"nameusn":nameusn, "sem": valueList[0][1],"result":result},  # not taking total here 
				sub1:{"sub":valueList[2][0],"ext":int(valueList[2][1]),"int":int(valueList[2][2]),"tot":int(valueList[2][3]),"passfail":sub1res},
				sub2:{"sub":valueList[3][0],"ext":int(valueList[3][1]),"int":int(valueList[3][2]),"tot":int(valueList[3][3]),"passfail":sub2res},
				sub3:{"sub":valueList[4][0],"ext":int(valueList[4][1]),"int":int(valueList[4][2]),"tot":int(valueList[4][3]),"passfail":sub3res},
				sub4:{"sub":valueList[5][0],"ext":int(valueList[5][1]),"int":int(valueList[5][2]),"tot":int(valueList[5][3]),"passfail":sub4res},
				sub5:{"sub":valueList[6][0],"ext":int(valueList[6][1]),"int":int(valueList[6][2]),"tot":int(valueList[6][3]),"passfail":sub5res},
				sub6:{"sub":valueList[7][0],"ext":int(valueList[7][1]),"int":int(valueList[7][2]),"tot":int(valueList[7][3]),"passfail":sub6res},
				sub7:{"sub":valueList[8][0],"ext":int(valueList[8][1]),"int":int(valueList[8][2]),"tot":int(valueList[8][3]),"passfail":sub7res},
				sub8:{"sub":valueList[9][0],"ext":int(valueList[9][1]),"int":int(valueList[9][2]),"tot":int(valueList[9][3]),"passfail":sub8res}
				}
		elif (found ==7):
			post = {"college": {"collegeName": collegeName, "collegeCode":collegeCode},
				"student":{"nameusn":nameusn, "sem": valueList[0][1],"result":result},  # not taking total here 
				sub1:{"sub":valueList[2][0],"ext":int(valueList[2][1]),"int":int(valueList[2][2]),"tot":int(valueList[2][3]),"passfail":sub1res},
				sub2:{"sub":valueList[3][0],"ext":int(valueList[3][1]),"int":int(valueList[3][2]),"tot":int(valueList[3][3]),"passfail":sub2res},
				sub3:{"sub":valueList[4][0],"ext":int(valueList[4][1]),"int":int(valueList[4][2]),"tot":int(valueList[4][3]),"passfail":sub3res},
				sub4:{"sub":valueList[5][0],"ext":int(valueList[5][1]),"int":int(valueList[5][2]),"tot":int(valueList[5][3]),"passfail":sub4res},
				sub5:{"sub":valueList[6][0],"ext":int(valueList[6][1]),"int":int(valueList[6][2]),"tot":int(valueList[6][3]),"passfail":sub5res},
				sub6:{"sub":valueList[7][0],"ext":int(valueList[7][1]),"int":int(valueList[7][2]),"tot":int(valueList[7][3]),"passfail":sub6res},
				sub7:{"sub":valueList[8][0],"ext":int(valueList[8][1]),"int":int(valueList[8][2]),"tot":int(valueList[8][3]),"passfail":sub7res}
				}
		elif (found ==6):
			post = {"college": {"collegeName": collegeName, "collegeCode":collegeCode},
			        "student":{"nameusn":nameusn, "sem": valueList[0][1],"result":result},  # not taking total here 
			        sub1:{"sub":valueList[2][0],"ext":int(valueList[2][1]),"int":int(valueList[2][2]),"tot":int(valueList[2][3]),"passfail":sub1res},
			        sub2:{"sub":valueList[3][0],"ext":int(valueList[3][1]),"int":int(valueList[3][2]),"tot":int(valueList[3][3]),"passfail":sub2res},
			        sub3:{"sub":valueList[4][0],"ext":int(valueList[4][1]),"int":int(valueList[4][2]),"tot":int(valueList[4][3]),"passfail":sub3res},
			        sub4:{"sub":valueList[5][0],"ext":int(valueList[5][1]),"int":int(valueList[5][2]),"tot":int(valueList[5][3]),"passfail":sub4res},
			        sub5:{"sub":valueList[6][0],"ext":int(valueList[6][1]),"int":int(valueList[6][2]),"tot":int(valueList[6][3]),"passfail":sub5res},
			        sub6:{"sub":valueList[7][0],"ext":int(valueList[7][1]),"int":int(valueList[7][2]),"tot":int(valueList[7][3]),"passfail":sub6res}
			        }
		elif (found ==5):
			post = {"college": {"collegeName": collegeName, "collegeCode":collegeCode},
			"student":{"nameusn":nameusn, "sem": valueList[0][1],"result":result},  # not taking total here 
			sub1:{"sub":valueList[2][0],"ext":int(valueList[2][1]),"int":int(valueList[2][2]),"tot":int(valueList[2][3]),"passfail":sub1res},
			sub2:{"sub":valueList[3][0],"ext":int(valueList[3][1]),"int":int(valueList[3][2]),"tot":int(valueList[3][3]),"passfail":sub2res},
			sub3:{"sub":valueList[4][0],"ext":int(valueList[4][1]),"int":int(valueList[4][2]),"tot":int(valueList[4][3]),"passfail":sub3res},
			sub4:{"sub":valueList[5][0],"ext":int(valueList[5][1]),"int":int(valueList[5][2]),"tot":int(valueList[5][3]),"passfail":sub4res},
			sub5:{"sub":valueList[6][0],"ext":int(valueList[6][1]),"int":int(valueList[6][2]),"tot":int(valueList[6][3]),"passfail":sub5res}
			}			
		elif (found==4):
			post = {"college": {"collegeName": collegeName, "collegeCode":collegeCode},
			"student":{"nameusn":nameusn, "sem": valueList[0][1],"result":result},  # not taking total here 
			sub1:{"sub":valueList[2][0],"ext":int(valueList[2][1]),"int":int(valueList[2][2]),"tot":int(valueList[2][3]),"passfail":sub1res},
			sub2:{"sub":valueList[3][0],"ext":int(valueList[3][1]),"int":int(valueList[3][2]),"tot":int(valueList[3][3]),"passfail":sub2res},
			sub3:{"sub":valueList[4][0],"ext":int(valueList[4][1]),"int":int(valueList[4][2]),"tot":int(valueList[4][3]),"passfail":sub3res},
			sub4:{"sub":valueList[5][0],"ext":int(valueList[5][1]),"int":int(valueList[5][2]),"tot":int(valueList[5][3]),"passfail":sub4res}
		        }			
		elif (found==3):
			post = {"college": {"collegeName": collegeName, "collegeCode":collegeCode},
		        "student":{"nameusn":nameusn, "sem": valueList[0][1],"result":result},  # not taking total here 
		        sub1:{"sub":valueList[2][0],"ext":int(valueList[2][1]),"int":int(valueList[2][2]),"tot":int(valueList[2][3]),"passfail":sub1res},
		        sub2:{"sub":valueList[3][0],"ext":int(valueList[3][1]),"int":int(valueList[3][2]),"tot":int(valueList[3][3]),"passfail":sub2res},
		        sub3:{"sub":valueList[4][0],"ext":int(valueList[4][1]),"int":int(valueList[4][2]),"tot":int(valueList[4][3]),"passfail":sub3res}
		        }
		elif (found==2):
			post = {"college": {"collegeName": collegeName, "collegeCode":collegeCode},
		        "student":{"nameusn":nameusn, "sem": valueList[0][1],"result":result},  # not taking total here 
		        sub1:{"sub":valueList[2][0],"ext":int(valueList[2][1]),"int":int(valueList[2][2]),"tot":int(valueList[2][3]),"passfail":sub1res},
		        sub2:{"sub":valueList[3][0],"ext":int(valueList[3][1]),"int":int(valueList[3][2]),"tot":int(valueList[3][3]),"passfail":sub2res}
		         
		        }
		elif (found==1):
			post = {"college": {"collegeName": collegeName, "collegeCode":collegeCode},
		        "student":{"nameusn":nameusn, "sem": valueList[0][1],"result":result},  # not taking total here 
		        sub1:{"sub":valueList[2][0],"ext":int(valueList[2][1]),"int":int(valueList[2][2]),"tot":int(valueList[2][3]),"passfail":sub1res}
		        
		        }			
	
		print "Inserting a document"
		collection.insert(post)
	
	#print "DBG: printing all records in the collection"
	#print "-------------------------------------------"
	#results=collection.find()
	#for record in results:
	#	print record
	client.close()	




if __name__=="__main__":

	valueList = []  # this is a list of lists
	sizeofVlist =0
	filecount=0     # no of files processed
	college = {}  # this is a dictionary that we will load from a CSV ( it will provide lookup for all VTU colleges)	
	
	# connect to MongoDB database "mydb"
	client = MongoClient('mongodb://localhost:27017/')
	db = client.vtu  # after testing we will change this db to vtu 
	collection = db.CS06
	
	
	
	
        #import all the collegeCodes into dictionary
	
	fname = "coursecollegeList.csv"
	
	f = open(fname, 'rb') # opens the csv file
	try:
	    reader = csv.reader(f)  # creates the reader object
	    for row in reader:   # iterates the rows of the file in orders
		print row    # prints each row college code : college name 
	finally:
	    f.close()      # closing
	
	reader = csv.reader(open(fname))
	    
	
	for row in reader:
		key = row[0]
		if key in college:
		    # implement your duplicate row handling here
		    pass
		college[key] = row[1:]
	#college.items() #print the dictionary for testing
	
	#====================================================
	# this code is for testing with single file 
		
	#fname="1AK14scs06.html"
	#print "The file being accessed :%s"%(fname)  #current filename to be processed 
	#process_file_updatedb(fname) # this does all the work 	
		
	#==========================================================		
	
	#the below code is for all files ; use this when you are using for all files 
	
	


	for file in os.listdir("C:/users/Admin/Desktop/PythonCode/CS6HTML"):
		#change the path for your testing or final run purpose
		if file.endswith(".html"):
			fname=file
			print "The file being accessed :%s"%(fname)  #current filename to be processed 
			process_file_updatedb(fname) # this does all the work 
			filecount +=1
			print "no of files processed: %d" % (filecount)
			#print "DBG: printing list of values..."
			#check_value(valueList)
	
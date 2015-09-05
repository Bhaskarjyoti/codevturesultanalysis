#last updated on 25/08 so that we can scrape the 4th semester results 
#========================================================================
#Last changed 23/08 evening 
#change in this code 
#(a) If the HTML is already in this directory, do nothing 
#(b) If the result is blank result, we remove the HTML to lessen the headache for next step 
#(c) We print the Number of USN we tried ( not files as some are getting deleted also)
#====================================================================================
#THIS CODE DOWNLOADS THE RESULT AS HTML FOR CS 04 SEMESTER 
#downloads based on two input file for a branch such as CSE B Tech (CS) 
#strength1.txt : no of students in the college (this information can be gleaned 
#from fastvturesults.com . It avoids doing unnecessary HTTP POST 
#collegelist1.txt : code name of the college such as '1RG'
#the rows in the two file can be aligned

#This is a modified code for CS students i.e. 1RG14CS001 

import mechanize
import cookielib
import time
import sys
import urllib2
import csv
import os
import re
from bs4 import BeautifulSoup
from random import randint

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# set working directory:
os.chdir("C:\Users\Admin\Desktop\PythonCode\CS4HTML")

#####  Open a website ##################


#strength.txt has the max roll no or no of students enrolled
with open('strength.txt') as f:
    maxrollno = f.read().splitlines()

#collegeList.txt has the college codes

with open('collegelist.txt') as f:
    collegeno = f.read().splitlines()

count = 0

for a,b in zip(collegeno,maxrollno):
    for i in range(1,int(b)+1):
        usn= (a+'13cs'+"%03d"%i).upper()  #changed here as per format 
        print (usn)
        count +=1
        #time.sleep(5)  
        sleeptime = randint(1,4)
        time.sleep(sleeptime)
        # Open some site:
        r = br.open('http://results.vtu.ac.in/')
	br._factory.is_html = True  # this we are doing to avoid checking proper HTML
        html = r.read()
        
         
        
        # Select the first (index zero) form
        # print("Selecting the first forms : ")
        
        br.select_form(nr=0)
            
        # Let's use that form 
        #print("Using the form for 1RG14SCS09 : ")
        
        br.form['rid']=usn
        br.submit()
        HTML_str=br.response().read()
        filename=usn+'.html'
	# if we already have this HTML, we do nothing. Else we write this
	if (os.path.exists(filename) == False):
	    print filename
	    Html_file= open(filename,"w")
	    Html_file.write(HTML_str)
	    '''
	    #now I will check if it is an empty result 
	    results = soup.find("td", {"width" : "513"})
	    #print results
	    tables = soup.findChildren('table')
	    my_table=tables[11]  # we are targetting the 11th table in soup
	    rows = my_table.find("td", {"width" : "513"}).findAll('tr')
	    number_of_rows = len(rows)
	    
	    #print ("number_of_rows")
	    #print number_of_rows
	    
	    if number_of_rows == 0:
		    print "The candidate has no result..removing the file" 
		    OS.remove(filename)
		    '''
	    Html_file.close()
	    
print ("total USN tried:" + str(count))    
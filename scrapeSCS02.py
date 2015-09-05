#last changed on 22/08 
# to accommodate the fact that some colleges have serial number greater than max no of students (strength has changed)
# to accommodate the fact that we should NOT download the result that we have already downloaded ( check for file exists )

#THIS CODE DOWNLOADS THE RESULT AS HTML FOR M TECH CSE 02 SEMESTER 
#downloads based on two input file for a branch such as CSE M Tech ( SCS) 
#strength.txt : no of students in the college (this information can be gleaned 
#from fastvturesults.com . It avoids doing unnecessary HTTP POST 
#collegelist.txt : code name of the college such as '1RG'
#the rows in the two file can be aligned

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
os.chdir("C:\Users\Admin\Desktop\PythonCode\SCSHTML")

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
        usn= (a+'14scs'+"%02d"%i).upper()
        
        print "USN Number is : %s"%(usn)
        count +=1
        filename=usn+'.html'
        if (os.path.exists(filename) == False):
            #time.sleep(5)  
            sleeptime = randint(2,9)
            time.sleep(sleeptime)
            # Open some site:
            r = br.open('http://results.vtu.ac.in/')
            html = r.read()
            
            '''
            # Show the html title
            # this commented part is for debugging
            print("This is the title of the website : ")
            print br.title()
            
            # Show the available forms
            print("These are the available forms : ")
            
            for f in br.forms():
                print f
                
            '''
            
            # Select the first (index zero) form
            # print("Selecting the first forms : ")
            
            br.select_form(nr=0)
                
            # Let's use that form 
            #print("Using the form for 1RG14SCS09 : ")
            
            br.form['rid']=usn
            br.submit()
            HTML_str=br.response().read()
            
            print filename
            Html_file= open(filename,"w")
            Html_file.write(HTML_str)
            Html_file.close()
        
print ("total number generated:" + str(count))    
#import necessary libraries
import os
import csv
import re
from langdetect import detect

#say hello
print("This script will perform analysis of several text files, searching for a list of provided terms and regular expressions.  You will be asked to provide a starting directory where all of your files are located, and a filepath/filename for your least of search terms.  The list must be a headerless CSV file.")
print()
proceedinput=input("Ready to continue? Enter 'Y' to proceed or 'N' to close this script: ")
if proceedinput in ('y','Y','yes','Yes','YES'):
    pass
elif proceedinput in ('n','N','no','No','NO','quit','Quit','QUIT','exit','Exit','EXIT','STOP','Stop','stop'):
    quit()
else:
    print('-----')
    print('PROBLEM WITH YOUR INPUT!  Re-run this script, and be sure to enter "Y" to run this script on the specified number of URLs or "N" to quit.')
    quit()

#get user inputs
dirinput=input("Where are all your plaintext files?  Put your starting directory here: ")
print()
searchlist=input("Where is your list of terms you want to search for?  Put the filepath and filename to the CSV file here: ")
print()

#open the list of search terms and turn it into a python list
print("Opening your list of terms...")
print()
termlist=[]
space=str(" ")
with open(searchlist, mode="r") as searchlist:
    rows = csv.reader(searchlist)
    for row in rows:
        term=row[0]
        term=space+term+space
        termlist.append(term)

#set up a results spreadsheet, write headers
resultheaders=['file','language']+termlist
csv_output = "diss-analysis-log.csv"
with open(csv_output, mode="w", newline="", encoding="utf8", errors="ignore") as outputlog:
    writer = csv.writer(outputlog, delimiter=",")
    writer.writerow(resultheaders)

#create a recursive list of files
print("Making a list of files to analyze...")
print()
if os.path.isdir(dirinput)==False:
    print()
    print('PROBLEM WITH STARTING DIRECTORY! It looks like',dirinput,'is not a valid location. Please make sure your file path is complete and does NOT end with a final slash, and then re-run this script.')
    quit()
else:
    filelist=[]
    def list_files_recursive(path='.'):
        for entry in os.listdir(path):
            filepath = os.path.join(path, entry)
            if os.path.isdir(filepath):
                list_files_recursive(filepath)
            else:
                filelist.append(filepath)
    list_files_recursive(dirinput)
#analyze each file in the list
print("Analyzing files and logging results...")
print()

for file in filelist:
    itemresult=[file]
    openfile=open(file,encoding='utf-8')
    opentext=openfile.read()
    openlang=detect(opentext)
    itemresult.append(openlang)
    for term in termlist:          
        counttermresult=opentext.count(term)
        itemresult.append(counttermresult) 
    #write itemresult to log
    with open (csv_output, mode="a",encoding="utf8", newline="",errors="ignore") as outputlog:
        writer = csv.writer(outputlog)
        writer.writerow(itemresult)

#say goodbye
print("Done!")
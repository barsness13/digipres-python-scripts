#import necessary libraries
import os
import csv
import re

#say hi
print("This script is meant to parse the text of dissertations in order to identify if and where the acknowledgements section, the table of contents, and systematic review sections might be; it also does basic error checking based on local dissertation formatting requirements.  It is designed to work automatically with the accompanying disstrimmer script, which will remove the body of a dissertation for easier analysis of the acknowledgements, provided the body of the dissertation is identified successfully by dissparser.")
print()
print("Dissparser will create a CSV output in the same location as the script, which shows where each section begins in the full text, as well as a truncation starting point for disstrimmer.  Please note that line numbers assume that the document starts with line ZERO rather than line ONE.  From a starting directory, it will create a list of all files in that directory, open each of them in turn, and search each one line by line.")
print()
print("For best results, provide a directory containing a working copy of your plaintext files and nothing else, as these same files may be edited by disstrimmer.  Additionally, it may be helpful to review the output log of dissparser before running disstrimmer to ensure it is working as expected.  To manually prevent a file from being truncated by disstrimmer, simply change the Truncation Start Line to 0.")
print()
dirinput=input("Starting directory: ")
print()

#create output log
csv_output = "diss-parser-log.csv"
with open(csv_output, mode="w", newline="", encoding="utf8", errors="ignore") as outputlog:
    writer = csv.writer(outputlog, delimiter=",")
    writer.writerow(["filename","ack start line","ToC start line","systematic review start line","abstract start line","truncation start line","result"])

#create a recursive list of files
if os.path.isdir(dirinput)==False:
    print()
    print("PROBLEM WITH STARTING DIRECTORY! It looks like",dirinput,"is not a valid location. Please make sure your file path is complete and does NOT end with a final slash, and then re-run this script.")
    quit()
else:
    filelist=[]
    def list_files_recursive(path="."):
        for entry in os.listdir(path):
            filepath = os.path.join(path, entry)
            if os.path.isdir(filepath):
                list_files_recursive(filepath)
            else:
                filelist.append(filepath)
    list_files_recursive(dirinput)

#go through each file in the list
for file in filelist:
    filename=str(file)
    ackline=0
    tocline=0
    sysrev=0
    abstract=0
    truncateline=0
    result="not processed"
    with open(filename,"r",encoding="utf-8") as readfile:
        for linenumber, linetext in enumerate(readfile):
            #find table of contents
            if tocline==0 and re.search(r"content",linetext,re.IGNORECASE):
                tocline=linenumber
                continue
                
            #check for an acknowledgements section       
            if ackline==0 and re.search(r"acknowledgement",linetext,re.IGNORECASE):
                ackline=linenumber
                continue
            
            if ackline==0 and re.search (r"acknowledgment",linetext,re.IGNORECASE):
                ackline=linenumber
                continue
            
            if ackline==0 and re.search (r"remerciements",linetext,re.IGNORECASE):
                ackline=linenumber
                continue
            
            if ackline==0 and re.search (r"agradecimientos",linetext,re.IGNORECASE):
                ackline=linenumber
                continue
            
            if ackline==0 and re.search (r"reconocimientos",linetext,re.IGNORECASE):
                ackline=linenumber
                continue
            
            #check for a systematic review section
            if sysrev==0 and re.search (r"systematic review",linetext,re.IGNORECASE):
                sysrev=linenumber
                continue
                
            #check for an abstract
            if abstract==0 and re.search(r"abstract",linetext,re.IGNORECASE):
                abstract=linenumber
                continue
 
            #write error notes if ToC, acknowledgements are missing or in unexpected order
            if ackline>tocline:
                truncateline=0
                result="manual review - acknowledgements after table of contents"
            elif ackline==0:
                result="manual review - no acknowledgements found"
            elif tocline==0:
                result="manual review - no table of contents found"
            
            #set the truncation point, make sure it's not suspiciously early in the document
            else:
                if abstract>0 and abstract<tocline:
                    truncateline=abstract+1
                    result="READY TO TRUNCATE"
                else:
                    truncateline=tocline+1
                    result="READY TO TRUNCATE"
                if truncateline<=30:
                    truncateline==0
                    result="manual review - truncation point suspiciously early"
                elif truncateline>=500:
                    truncateline==0
                    result="manual review - truncation point suspiciously late"

    #write information to log
    itemlog=[filename,ackline,tocline,sysrev,abstract,truncateline,result]
    with open (csv_output, mode="a",encoding="utf8", newline="",errors="ignore") as outputlog:
        writer = csv.writer(outputlog)
        writer.writerow(itemlog)

print("Done!")
#import libraries and set up data structures
import csv
import re
import os

#say hi, confirm it's time to run
print("This script will tidy up text files to remove nonprinting characters that can cause problems for text analysis like newlines, multiple spaces, and tabs.  Simply point it at a folder where all your caption files are saved, and it will automatically clean up all the .txt files in that directory and it's subdirectories.")
print()
dirinput=input('Starting directory: ')
if os.path.isdir(dirinput)==False:
    print()
    print('PROBLEM WITH STARTING DIRECTORY! It looks like',dirinput,'is not a valid location. Please make sure your file path is complete and does NOT end with a final slash.')
    quit()

#create a recursive file list
else:
    print("making a list of text files in that location...")
    filelist=[]
    filecount=0
    TXTlist=[]
    TXTcount=0
    skiplist=[]
    skipcount=0
    def list_files_recursive(path='.'):
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                list_files_recursive(full_path)
            else:
                filelist.append(full_path)
    list_files_recursive(dirinput)
    
#iterate through each file in list, grouping by format
for file in filelist:

    #put TXT files into one list
    if bool(re.search("[.][t][x][t]$", file)):
        filecount=filecount+1
        TXTcount=TXTcount+1
        TXTlist.append(file)
    #put everything else into a skip list
    else:
        filecount=filecount+1
        skipcount=skipcount+1
        skiplist.append(file)

#print file counts and get confirmation before proceeding
print('We checked ',filecount,' files and found:')
print(TXTcount,' TXT files')
print(skipcount,' other files will be skipped')
print()
proceedinput=input('Are you ready to proceed? Enter "Y" to proceed or "N" to close this script: ')
if proceedinput in ('y','Y','yes','Yes','YES'):
    pass
elif proceedinput in ('n','N','no','No','NO','quit','Quit','QUIT','exit','Exit','EXIT','STOP','Stop','stop'):
    quit()
else:
    print('-----')
    print('PROBLEM WITH YOUR INPUT!  Re-run this script, and be sure to enter "Y" to run this script on the specified number of URLs or "N" to quit.')
    quit()

print("Processing...")
print()

#open txt files and trim nonprinting characters
for TXT in TXTlist:
    editfile=str(TXT)
    writefile=str(TXT)
    with open(editfile,"r",encoding="utf-8", errors='ignore') as editfile:
        newtext=editfile.read().replace('\n',' ')
    writetext=re.sub(' +', ' ',newtext)
    with open(writefile,"w",encoding="utf-8",errors='ignore') as writefile:
        writefile.write(writetext)
print("Done!")
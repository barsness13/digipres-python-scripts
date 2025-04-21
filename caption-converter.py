#import libraries
import os
import re
import srt_to_vtt
from vtt_to_srt.vtt_to_srt import ConvertFile
from pathlib import Path

#get starting directory from user, validate, create a recursive file list
dirinput=input('Starting directory: ')
if os.path.isdir(dirinput)==False:
    print()
    print('PROBLEM WITH STARTING DIRECTORY! It looks like',dirinput,'is not a valid location. Please make sure your file path is complete and does NOT end with a final slash.')
    quit()
else:
    filelist=[]
    filecount=0
    VTTlist=[]
    VTTcount=0
    SRTlist=[]
    SRTcount=0
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

    #put SRT files into one list
    if bool(re.search("[.][s][r][t]$", file)):
        filecount=filecount+1
        SRTcount=SRTcount+1
        SRTlist.append(file)
        
    #put VTT files into one list
    elif bool(re.search("[.][v][t][t]$", file)):
        filecount=filecount+1
        VTTcount=VTTcount+1
        VTTlist.append(file)
        
    #put everything else into a skip list
    else:
        filecount=filecount+1
        skipcount=skipcount+1
        skiplist.append(file)

#print file counts and get confirmation before proceeding
print('We checked ',filecount,' files and found:')
print(SRTcount,' SRT files')
print(VTTcount,' VTT files')
print(skipcount,' other files will be skipped')
print('-----')
proceedinput=input('Are you ready to proceed? Enter "Y" to proceed or "N" to close this script: ')
if proceedinput in ('y','Y','yes','Yes','YES'):
    pass
elif proceedinput in ('n','N','no','No','NO'):
    quit()
else:
    print('-----')
    print('PROBLEM WITH YOUR INPUT!  Re-run this script, and be sure to enter "Y" to run this script on the specified number of URLs or "N" to quit.')
    quit()

print("Processing...")

#convert SRT list to VTT
for SRT in SRTlist:
    VTT=SRT[:-4]+'.vtt'
    srt_to_vtt.srt_to_vtt(SRT,VTT)
    
#Convert VTT list to SRT
for VTT in VTTlist:
    SRT=ConvertFile(VTT, "utf-8")
    SRT.convert()
    
#Make transcripts from VTT files
#re-check starting directory for all files
newfilelist=[]
newVTTlist=[]
def list_files_recursive(path='.'):
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                list_files_recursive(full_path)
            else:
                newfilelist.append(full_path)
list_files_recursive(dirinput)

#make a list of all VTT files
for newfile in newfilelist:
    if bool(re.search("[.][v][t][t]$", newfile)):
        newVTTlist.append(newfile)
        
    else:
        pass

#convert VTT files to transcripts
for newVTT in newVTTlist:
    textpath=newVTT.replace(".vtt",".txt")
    textpath=Path(textpath)
    textlines=[]
    with open(newVTT) as vtt:
        alllines=vtt.readlines()
    for line in alllines:
        if line.startswith('WEBVTT'):
            pass
        elif bool(re.search("^[0-9][0-9][:][0-9][0-9][:][0-9][0-9][.][0-9][0-9][0-9][ ][-][-][>]",line)):
            pass
        else:
            textlines.append(line)
    with open(textpath, "w") as textfile:
        for line in textlines:
            textfile.write(line)
print("Done!  This script has converted ",VTTcount," VTT files to SRT and plaintext, and ",SRTcount," SRT files to VTT and plaintext")
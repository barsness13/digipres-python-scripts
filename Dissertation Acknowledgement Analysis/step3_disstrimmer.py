#import libraries and set up data structures
import csv
truncatelist={}

#say hi, confirm it's time to run
print("This script works in conjunction with dissparser to truncate dissertations to remove the body and bibliography, leaving the acknowledgements and as little other frontmatter as possible.  It will automatically run using the output log from dissparser, so ensure that your files have not moved between running dissparser and disstrimmer.  Additionally, dissparser's output log (called 'diss-parser-log.csv') should be saved in the same location as the dissparser and disstrimmer scripts.  You may want to review the log before running disstrimmer.")
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
    
print("Working...")

#open dissparser log and review for files to trim
with open("diss-parser-log.csv", mode="r") as disslog:
    rows = csv.reader(disslog)
    for row in rows:
        try:
            truncateline=int(row[5])
        except:
            continue
        if truncateline>0: 
            filename=str(row[0])
            newtrimfile={filename:truncateline}
            truncatelist.update(newtrimfile)
                       
#for each file in the list, open it and re-write in each line until the truncate point
for trimfile, trimline in truncatelist.items():
    editname=str(trimfile)
    cutline=int(trimline)
    newtext=list()
    
    with open(editname,"r",encoding="utf-8", errors='ignore') as editfile:
        for editline, edittext in enumerate(editfile):
            if editline<cutline:
                newtext.append(edittext)
            else:
                break
    
    with open (editname,"w",encoding="utf-8",errors='ignore') as editfile:
        for line in newtext:
            editfile.write(line)

print("Done!")
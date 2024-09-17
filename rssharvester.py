#import libraries
import feedparser
import csv
import re
import time

#print explanatory text and instructions
print('-----')
print('Welcome!  This script is written to parse RSS feeds for podcasts and convert selected metadata elements into a CSV spreadsheet.  This script was written at the University of Minnesota, so the output formatted for ingesting into our Institutional Repository, but may have uses well beyond that.  Formatting is more or less basic Dublic Core metadata in a CSV file, with some extra DSpace-specific fields added.')
print()
print("You can run this script for a single podcast, or for several podcasts at once.  To run on a single podcast, you'll need the URL for the podcast's RSS feed.  You'll also need to provide a title for the resulting CSV. To run this script for several podcasts at once, you'll need a CSV file with the RSS URL in Column A, and the desired title for the output log in Column B.  There should be no header rows.")
print()


#determine starting input (single URL or csv file list)
print('-----')
styleinput=input('Would you like to run this script by providing a single RSS URL, or would you like to run it on a CSV with RSS URLs?  Enter "1" for a single URL or "2" for a multi-URL csv: ')
print()
if styleinput in ('1','one','One','ONE'):
    #get starting RSS URL from user, establish output filename
    inname=input('Enter RSS URL: ')
    outname=input('Enter the desired filename for the output CSV: ')
    feedlist={inname:outname}
    rowcounter=1
elif styleinput in ('2','two','Two','TWO'):
    #get filepath to CSV from user, establish list of input URLs and output filenames
    csv_input = input("Enter the filepath and name of the input CSV: ")
    feedlist={}
    with open(csv_input, mode='r', encoding="utf8", errors='ignore') as userinput:
        reader = csv.DictReader(userinput)
        rowcounter=0
        for row in csv.reader(userinput):
            inname=row[0]
            outname=row[1]
            feedlist[inname]=outname
            rowcounter=rowcounter+1
else:
    print('-----')
    print('PROBLEM WITH YOUR INPUT!  Re-run this script, and be sure to enter "1" to run this script on a single RSS URL or "2" to start with a CSV list.')
    quit()

#show user number of feeds to be parsed, confirm before proceeding
print('-----')
print('This script is about to parse ',rowcounter,' RSS feeds.')  
proceedinput=input('Are you ready to proceed? Enter "Y" to proceed or "N" to close this script: ')
if proceedinput in ('y','Y','yes','Yes','YES'):
    pass
elif proceedinput in ('n','N','no','No','NO'):
    quit()
else:
    print('-----')
    print('PROBLEM WITH YOUR INPUT!  Re-run this script, and be sure to enter "Y" to run this script on the specified number of URLs or "N" to quit.')
    quit()

print('-----')
print('Processing...')
print()

for key in feedlist:
    logname=feedlist[key]
    feed=feedparser.parse(key)
    
    #skip extraction if no entries found
    if len(feed['entries'])==0:
        print('-----')
        print('There was an unexpected problem pulling data from ',inname,'. This URL has been skipped.')
        print('Processing...')
        print()
        continue
    else:
        #set up CSV file and header row
        import csv
        with open(logname, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['dc.title', 'dc.date.issued', 'dc.description.abstract', 'dc.description', 'filename-audio', 'filename-image','dc.type.','dc.contributor.author','id','collection'])
        
        #get default image value
        try:
            defaultthumb=feed.feed.image['href']
        except:
            defaultthumb="No Image Available"
        
        #validating each entry in RSS and converting into variables
        for entry in feed.entries:
            try:
                title=entry.title
            except:
                title="No Title Available"
            try:
                parseddate=entry.published_parsed
                date=time.strftime('%Y-%m-%d',parseddate)
            except:
                date="No Date Available"
            try:
                abstract=entry.description
            except:
                abstract="No Abstract Available"
            try:
                description=entry.itunes_duration
            except:
                description="No Runtime Available"
            try:
                files=entry.enclosures[0]['href']
            except:
                files="No Files Available"
            try:
                image=entry.image['href']
            except:
                try:
                    image=defaultthumb
                except:
                    image="No Image Available"
            type="Audio"

        
        #write entry metadata into a new row
            entrydata=[title, date, abstract, description, files, image, type]
            with open(logname, mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(entrydata)

print()
print('Process is completed!')

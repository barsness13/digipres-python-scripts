#import libraries
import csv
import os
from urllib.request import urlopen
import json

#get filepath to CSV from user
print()
print('Welcome!  This script will help you download the TEXT bundle for items in the UDC.  The required input is a CSV with a links of item UUIDs in column A.  UUIDs should NOT be formatted as URLS (e.g., use 20d78d84-5339-44d8-bbae-0d76eff7d630 instead of conservancy.umn.edu/items/20d78d84-5339-44d8-bbae-0d76eff7d630.  The CSV should NOT have a header row.')
print()
csv_input = input("Enter the filepath of the input CSV: ")
print()
print('This script will log its activities, including any naming issues or errors, in a new CSV.  You will need to provide a desired filepath and filename for this log.')
print()
csv_output = input("Enter the filepath/name for the log file:")
itemcount=0
failcount=0
log=[]
log.append(["UUID","FILENAME","RESULT"])
print()
print('Fetching TEXT bundles...')

with open(csv_input, mode='r', newline='', encoding="utf8", errors='ignore') as userinput:
    for row in csv.reader(userinput):
        uuid=row[0]
        itemAPI=str("https://conservancy.umn.edu/server/api/core/items/"+uuid+"/bundles")

        #retrieve and parse resulting JSON
        try:
            itemresponse=urlopen(itemAPI)
            itemdata=json.loads(itemresponse.read())
            itembundles=itemdata["_embedded"]["bundles"]
            for item in itembundles:
                if item["name"]=="TEXT":
                    textAPI=str(item["_links"]["bitstreams"]["href"])
                else:
                    continue  
            #load and parse the JSON data for the item's text bundle
            try:
                bundleresponse=urlopen(textAPI)
                bundledata=json.loads(bundleresponse.read())
                bundlefiles=bundledata["_embedded"]["bitstreams"]
                #for each file in the text bundle, get data and save as a text file
                for file in bundlefiles:
                    filename=str(uuid+"_"+file["name"])
                    textlocation=str(file["_links"]["content"]["href"])
                    try:
                        textresponse=urlopen(textlocation)
                        textcontent=textresponse.read()
                        finaltext=textcontent.decode()
                    except:
                        logentry=[uuid,filename,"ERROR - could not retrieve content of text bundle!"]
                        failcount=failcount+1
                        continue
                    if len(finaltext)==0:
                        logentry=[uuid,filename,"ERROR - empty text file!"]
                        failcount=failcount+1
                        continue
                    else:
                        with open(filename,"w",encoding="utf-8") as textfile:
                            textfile.write(finaltext)
                        logentry=[uuid,filename,"success"]
                        itemcount=itemcount+1    
            except:
                logentry=[uuid,"--","ERROR! - could not retrieve text bundles"]
                failcount=failcount+1
                continue
        except:
            logentry=[uuid,"--","ERROR! - could not open item record"]
            failcount=failcount+1
            continue
        log.append(logentry)

#create output CSV, write header row
with open(csv_output, mode='a', newline='', encoding="utf8", errors='ignore') as outputlog:
    writer = csv.writer(outputlog, delimiter=',')
    writer.writerows(log)
    
print("done! ",itemcount,"text files retrieved and ",failcount,"files failed.")
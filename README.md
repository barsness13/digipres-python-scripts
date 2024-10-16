# digipres-python-scripts
Python scripts for UDC and digital preservation tasks

## rssharvester.py
- written for Python 3.12.1
- uses the following libraries:
  - feedparser (https://pypi.org/project/feedparser/)
  - csv
  - re
  - time
- requires user to provide -EITHER- a single RSS URL and a filepath/filename for the resulting output -OR- a headerless CSV with several RSS URLs in column A and filepaths/filenames for outputs in column B
- creates one csv per URL in the specified location; if no location is provided files are saved in the same location as the script.  Each file represents one RSS feed, and each line represents a single entry/episode in the feed
- output column headers are labelled with the Dublin Core metadata element used in our instance of DSpace (including the collection and id columns DSpace requires for bulk ingests)
- most data should be relatively clean, but description field may contain HTML markup that needs to be stripped/reformatted
- to download images and audio files, I currently use Chrome extensions to bulk open URLs in new tabs and to bulk download
  - Open Multiple URLs: https://github.com/htrinter/Open-Multiple-URLs/ and https://chromewebstore.google.com/detail/open-multiple-urls/oifijhaokejakekmnjmphonojcfkpbbh
  - Down Them All: https://www.downthemall.net/
- known issues/future development ideas:
  - add cleanup of HTML elements in description field
  - add a date cutoff to ignore episodes older than a given date
  - integrate optional download of image and audio files

## filepath-validator.py
- written for Python 3.12.1
- requires user to provide EITHER a CSV file (with a list of filepaths/filenames in column A) OR a starting directory (which the script searches recursively to create a file list)
- checks each file for...
  -  a well-formed extension (a period with 3 characters)
  -  one and only one period
  -  no whitespace or nonprinting characters
  -  characters outside of a-z, A-Z, 0-9, dash, underscore, backslash, and period
  -  0 or 1 colon (allow for relative and absolute filepaths)
- creates a csv in the same location where the script is saved; file contains the file list as well as each potential issue in its own column (e.g., extension issues are noted in column B and whitespace issues are noted in column C).
- known issues: 
  -  may return false positives for accepted 4-character extensions (e.g., JPEG or TIFF)

## csv-rename-and-move.py
- written for Python 3.12.1
- requires a CSV with a current filepath and filename in column A, and a desired filepath/filename in column B
- checks that the new path/filename isn't already taken and checks each new path/name for quality (see filepath-validator.py)
- skipping any of those potential problems, it will create any directories that are needed and move/rename files
- gives a summary of files found, successes, and errors
- creates a log with a file-by-file summary of changes

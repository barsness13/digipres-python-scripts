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

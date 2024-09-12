# digipres-python-scripts
Python scripts for UDC and digital preservation tasks

## rssharvester.py
- written for Python 3.12.1
- requires user to provide -EITHER- a signle RSS URL and a filename for the resulting output -OR- a headerless CSV with several RSS URLs in column A and filenames for outputs in column B
- creates a csv of the desiered in the same location where the script is saved; file contains all rss data where each row is one episode
- output column headers are labelled with the Dublin Core metadata element used in the UDC
- cells will require cleanup and review before they're ready to do anything with
- to download images and audio files, I use Chrome extensions to bulk open URLs in new tabs and to bulk download
- known issues:
  -  resulting metadata requires substantial cleanup that could be minimized in the code (e.g., parsing attachment data to return only URLs rather than the whole tag)
  -  may not work if rss feed doesn't meet common syndication requirements (e.g., apple podcasts)

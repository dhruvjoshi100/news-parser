import os
import csv
import requests
import sys
import xml.etree.ElementTree as ET
 

rootdirectory= os.path.join(os.path.dirname(os.path.realpath(__file__)),'news/')	

fields = ['title', 'pubDate', 'link']

# load the given RSS feed and save it  to XML file
def RSSfeed(src,filename):

	src=src.rstrip()
	req = requests.get(str(src))
   	print "Loaded feed "+src
   	with open(filename, 'wb') as f:
   		f.write(req.content)
      
# method names say it all
def XMLparser(xmlfile):
 
    tree = ET.parse(xmlfile)
 
    root = tree.getroot()
 
    newsitems = []
    for item in root.findall('./channel/item'):
 
        news = {}
 
        for child in item:

            for s in fields:
                if child.tag==s:
                    news[child.tag] = child.text.encode('utf8')
 
        newsitems.append(news)
     
    return newsitems
 
def savetoCSV(newsitems, filename):
 
    with open(filename, 'w') as csvfile:
 
        writer = csv.DictWriter(csvfile, fieldnames = fields)
 
        writer.writeheader()
        writer.writerows(newsitems)

# clears old , pre-existing files to be replaced by updated files 
def clear():

    for root, sub, f in os.walk(rootdirectory):
        for f1 in f:
            if f1 != 'source.txt':
                os.remove(os.path.join(root,f1))
 

# to traverse through the diectory structure
def fetch():

	clear()

	for root, sub, f in os.walk(rootdirectory):
	    for f1 in f:
	        if f1=='source.txt':
	            src=""

	            with open(os.path.join(root,f1),'r') as f2:
	                src=f2.readline()

	            RSSfeed(src,os.path.join(root,"newsfeed.xml"))
	            newsitems = XMLparser(os.path.join(root,"newsfeed.xml"))
	            savetoCSV(newsitems,os.path.join(root,"newsfeed.csv"))

	print '\nData updated. Navigate thorugh the respective directories to find the latest news in the CSV files.'
     
def main():
    fetch() 
     
if __name__ == "__main__":
     main()

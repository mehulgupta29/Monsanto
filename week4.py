"""
A scrip that reads a file from the web and return the three most frequent words in the file
"""

import re
import time
from nltk.corpus import stopwords
import urllib2
from operator import itemgetter


def run(url): 

	freq={} # keep the freq of each word in the file 

	stopLex=set(stopwords.words('english')) # build a set of english stopwrods 

	#make a new browser, this will download pages from the web for us. This is done by calling the 
	#build_opener() method from the urllib2 library
	browser=urllib2.build_opener()

	#desguise the browser, so that websites think it is an actual browser running on a computer
	browser.addheaders=[('User-agent', 'Mozilla/5.0')]

	success=False# become True when we get the file

	for i in range(5): # try 5 times

		try:
        		#use the browser to access the url
	        	response=browser.open(url)    
			success=True # success
			break # we got the file, break the loop
		except:# browser.open() threw an exception, the attempt to get the response failed
			print 'failed attempt',i


	# all five attempts failed, return  None
	if not success: return None

	text=response.read()# read in the text from the file

	sentences=text.split('.') # split the text into sentences 
	
	for sentence in sentences: # for each sentence 

		sentence=sentence.lower().strip() # loewr case and strip
		
		sentence=re.sub('[^a-z]',' ',sentence) # replace all non-letter characters  with a space
		
		words=sentence.split(' ') # split to get the words in the sentence 

		for word in words: # for each word in the sentence 
			
			if word=='' or word in stopLex:continue # ignore empty words and stopwords 
		
			else: freq[word]=freq.get(word,0)+1 # update the frequency of the word 
	
	
	# sort the dictionary by value, in descending order 
	sortedByValue=sorted(freq.items(),key=itemgetter(1),reverse=True)

	return sortedByValue[0:3] # return the top 3 terms and their frequencies 



if __name__=='__main__':
	print run('http://tedlappas.com/wp-content/uploads/2016/09/textfile.txt')
	

	

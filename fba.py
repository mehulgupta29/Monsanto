
#import urllib.request as ulr
#import urllib2 as ulr
import requests as r
import xmltodict
from operator import itemgetter
import json
import csv

def fetchData(url):
	"""
	"""
	#make a new browser, this will download pages from the web for us. This is done by calling the 
	#build_opener() method from the urllib2 library
	#browser=ulr.build_opener()

	#desguise the browser, so that websites think it is an actual browser running on a computer
	#browser.addheaders=[('User-agent', 'Safari/537.36')]

	success=False# become True when we get the file

	for i in range(5): # try 5 times

		try:
			#use the browser to access the url
			#response=browser.open(url)    
			response=r.get(url)
			success=True # success
			break # we got the file, break the loop
		except:# browser.open() threw an exception, the attempt to get the response failed
			print('failed attempt',i)

	# all five attempts failed, return  None
	if not success: return None

	fbaDraftProjections=response.text
	return fbaDraftProjections	

def convertXMLToPY(xmlData):
	"""
	"""
	pyData=[]
	tempdict=dict(xmltodict.parse(xmlData)['FantasyBasketballNerd'])
	for d in tempdict['Player']:
		pyData.append(dict(d))

	return pyData

def calculateWinScore(PTS, REB, STL, AST, BLK, THREES, FG, TO, FT, GAMES):
	"""
	"""
	FGA=(((PTS - 3*THREES)*0.45)/FG)
	FTA=(((PTS - 3*THREES)*0.1)/FT)
	WS=((PTS)+(REB)+(STL)+(0.5*AST)+(0.5*BLK)-(FGA)-(TO)-(0.5*FTA))/GAMES

	return WS

def computeWinScore(fbaList):
	"""
	output:
		byPositions={position: {playerId: winscore, playerId2: winscore2, ....}}
		playerNamesDict={pid: playerName, ...}
	"""
	byPositions={}
	playerNamesDict={}
	for fba in fbaList:
		pos=fba['position']
		pid=fba['playerId']

		playerDict={pid: calculateWinScore(float(fba['PTS']), float(fba['REB']), float(fba['STL']), float(fba['AST']), float(fba['BLK']), float(fba['THREES']), float(fba['FG']), float(fba['TO']), float(fba['FT']), float(fba['Games']))}

		if pos in byPositions:
			byPositions[pos][pid]=calculateWinScore(float(fba['PTS']), float(fba['REB']), float(fba['STL']), float(fba['AST']), float(fba['BLK']), float(fba['THREES']), float(fba['FG']), float(fba['TO']), float(fba['FT']), float(fba['Games']))
		else:
			byPositions[pos]=playerDict

		playerNamesDict[pid]=fba['name']

	return byPositions,playerNamesDict

def getPlayerName(pid, playerNamesDict):
	"""
	"""
	return playerNamesDict[pid]


def findTopPlayerByPosition(byPositions, playerNamesDict):
	"""
	input:
		byPositions={position: {playerId: winscore, playerId2: winscore2, ....}, ...}
		playerNamesDict={pid: playerName, ...}
	variables:
		sortedByValue=[(pid, winscore), (), ...]
	output:
		results={position: (playerName, winscore), ...}
	"""
	results={}
	for pos, playerDict in byPositions.items():
		sortedByValue=sorted(playerDict.items(), key=itemgetter(1), reverse=True)
		sortedByValue=sortedByValue[:1][0]
		results[pos]=(getPlayerName(sortedByValue[0], playerNamesDict), sortedByValue[1])
	return results

def getAllPositions(fbaList):
	"""
	"""
	result=[]
	for fba in fbaList:
		if fba['position'] not in result:
			result.append(fba['position'])
	print(result)


def convertToCSV(fname, data):
	"""
		convert a python list to csv and write it to a file
	"""
	key=[]
	f = csv.writer(open(fname, "w"))
	
	#Write CSV Header, If you dont need that, remove this line
	key.append('position')
	key.append('player name')
	key.append('win score')
	f.writerow(key)

	#Write the data to csv
	for pos, value in data.items():
		res=[]
		res.append(pos)
		res.append(value[0])
		res.append(value[1])
		f.writerow(res)
	print(fname, "successfully created")

def writeToFile(fname, data):
	"""
	"""

	data=json.dumps(data)
	fw=open(fname, 'w')
	fw.write(data)
	fw.close()


def run(url): 
	"""

	variables:
		fbaDraftProjections: text
		fbaList=[{'name': playerName, 'playerId': pid, ..}, ...]
		results={position: {playerId: winscore, playerId2: winscore2, ....}}
		results={position: (playerName, winscore), ...}
	"""
	fbaDraftProjections=fetchData(url)
	if fbaDraftProjections != None:
		print("Fetch Successful")
		fbaList=convertXMLToPY(fbaDraftProjections)
		results,playerNamesDict=computeWinScore(fbaList)
		results=findTopPlayerByPosition(results, playerNamesDict)
		print(results)

		#writeToFile('output.json', results)
		convertToCSV('output.csv', results)
	else:
		print("Error")

	#getAllPositions(fbaList)
	

if __name__=='__main__':
	run('https://www.fantasybasketballnerd.com/service/draft-projections')

	

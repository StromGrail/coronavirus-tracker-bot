from notify_run import Notify
import requests
import json
from bs4 import BeautifulSoup 

class CoronaNotification():
	def __init__(self):
		super(CoronaNotification, self).__init__()
		
	def sendNotification(self, updatedValue):
		with open("temp.txt") as f:
			with open("history.txt", "w") as f1:
				for line in f:
					f1.write(line) 
		try:
			self.notify = Notify()
			self.notify.send("New cases in "+updatedValue,'https:\\\\www.mohfw.gov.in\\')
		except Exception as e:
			print(e)

	def fetchDataFromGovtSite(self):
		url = 'https://www.mohfw.gov.in/'
		resp = requests.get(url)
		if resp.status_code == 200:
			soup=BeautifulSoup(resp.text,'html.parser')
			tableBody=soup.find("tbody")
			row = tableBody.findAll('td')
			index, isDataChanged, updatedValue=0,False, ""
			historyFile = open("history.txt",'r+')
			tempFile = open("temp.txt",'w')
			jsonData=json.dumps({})
			while index < len(row)-6:
				historyData = historyFile.readline()
				
				currentData = json.dumps({"StateName": str(row[index+1].contents[0]),
								"TotalIndian":  	   int(row[index+2].contents[0]),
								"TotalForeign": 	   int(row[index+3].contents[0]),
								"TotalCured":   	   int(row[index+4].contents[0]),
								"TotalDeath":   	   int(row[index+5].contents[0])
								})
				
				tempFile.write(currentData+'\n')

				if historyData[:len(historyData)-1]!=currentData:
					isDataChanged=True
					updatedValue += json.loads(currentData)["StateName"]+', '

				index+=6
			tempFile.close()
			historyFile.close()

			if isDataChanged:
				self.sendNotification(updatedValue[ : (len(updatedValue)-2) ])

if __name__ == '__main__':
	coronaReport= CoronaNotification()
	coronaReport.fetchDataFromGovtSite()
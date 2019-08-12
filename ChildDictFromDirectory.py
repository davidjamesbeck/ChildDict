import os
import yattag


class EntryObject:

	def __init__(self, partList):
		self.textFile = partList[0]
		with open(self.textFile, 'r') as f:
			text = f.read()
			self.entry = text.split('\t')
		for i in range(1,len(partList)):
			if i[:-4] == ".wav":
				self.sound = i
			else:
				self.otherResource = i
		self.headword = self.getHeadword()
		self.definition = self.getDef()
		self.topic = self.getTopic()
		
	def getHeadword(self):
		return(self.entry[0])

	def getDef(self):
		return(self.entry[1])
		
	def getTopic(self):
		return(self.entry[2])
		
def makeHTML(list):
	htmlDoc = yattag.Doc()
	timeCodesForText = []
	htmlDoc.asis('<!DOCTYPE html>')
	with htmlDoc.tag('html', lang="en"):
		with htmlDoc.tag('head'):
			htmlDoc.asis('<meta charset="UTF-8">')
# 			htmlDoc.asis(self.getJQuery())
# 			htmlDoc.asis(self.getCSS())
			with htmlDoc.tag('body'):
				for item in list:
					with htmlDoc.tag("div",  klass="entry"):
						with htmlDoc.tag("div",  klass="headword"):
							htmlDoc.asis(item.headword)
						with htmlDoc.tag("div",  klass="definition"):
							htmlDoc.asis(item.definition)
	htmlText = htmlDoc.getvalue()
	return(htmlText)
		
textFileList = []
entryList = []
for filename in os.listdir("."):
    if filename[-4:] == ".txt":
        textFileList.append(filename)

for file in textFileList:
	partList = []
	for i in os.listdir("."):
		if file in i:
			partList.append(i)
		if len(partList) >= 1:
			entryList.append(EntryObject(partList))
	print(entryList[0].headword, entryList[0].definition,entryList[0].topic)
page = makeHTML(entryList)
print(page)

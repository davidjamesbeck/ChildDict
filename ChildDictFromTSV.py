import os, argparse
import yattag


class EntryObject:
	'''written assuming five columns—topic subtopic headword definition soundfile, 
	soundfile is optional'''
	def __init__(self, entry):
		memberList = entry.split('\t')
		self.topic = memberList[0]
		self.subtopic = memberList[1]
		self.headword = memberList[2]
		self.definition = memberList[3]
		if len(memberList) >= 5 and len(memberList[4]) != 0:
			self.soundfile = memberList[4]
		else:
			self.soundfile = None

def getCSS():
	cssFilename = "childDict.css"
	assert(os.path.exists(cssFilename))
	css = '<link rel = "stylesheet" type = "text/css" href = "%s" />' % cssFilename
	return(css)	

def getJava():
	script = '''function playSample(audioID)
{
	var audio = new Audio(audioID);
	audio.play();
}'''
	scriptTag = "<script>%s</script>\n" %script
	return(scriptTag)
			
def makeHTML(list):
	htmlDoc = yattag.Doc()
	currentTopic = 'start'
	currentSubtopic = 'start'	
	htmlDoc.asis('<!DOCTYPE html>')
	with htmlDoc.tag('html', lang="en"):
		with htmlDoc.tag('head'):
			htmlDoc.asis('<meta charset="UTF-8">')
			htmlDoc.asis(getJava())
			htmlDoc.asis(getCSS())
		with htmlDoc.tag('body'):
			for item in list:
				if currentTopic != item.topic:
					with htmlDoc.tag("H1"):
						htmlDoc.text(item.topic)
						currentTopic = item.topic
				if currentSubtopic != item.subtopic:
					with htmlDoc.tag("H2"):
						htmlDoc.text(item.subtopic)
						currentSubtopic = item.subtopic
				with htmlDoc.tag("div",  klass="entry"):
					with htmlDoc.tag("div",  klass="headword"):
						if item.soundfile:
							audioFile = "audio/%s" %item.soundfile
							with htmlDoc.tag("div", klass="linkedheadword", onclick="playSample('%s')" %audioFile):
								htmlDoc.text(item.headword)
						else:
							htmlDoc.text(item.headword)
					with htmlDoc.tag("div",  klass="definition"):
							htmlDoc.text(item.definition)
	htmlText = htmlDoc.getvalue()
	return(htmlText)

parser = argparse.ArgumentParser()
parser.add_argument('dictFile')
args = parser.parse_args()
dictFile = args.dictFile
path = os.path.dirname(os.path.abspath(__file__))
pathtofile = os.path.join(path,dictFile)
with open(pathtofile,'r') as dict:
	dictionaryData = dict.read()
	
entryList = dictionaryData.split('\n')[1:]
# sortedEntryList = sorted(entryList, key=lambda entryList[0]: (entryList[1](entryList[0]), entryList[0]))
objectList = []
for entry in entryList:
	o = EntryObject(entry) 
	objectList.append(o)
page = makeHTML(objectList)
with open('childDict.html','w') as f:
	f.write(page)
os.system("open %s" %'childDict.html')
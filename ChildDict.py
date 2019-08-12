import os, argparse
import yattag


class IndexEntry:
    '''class defines an entry for the navigation sidebar'''
    def __init__(self, pagename, subtopic, topic, supertopic):
        self.topic = topic
        self.subtopic = subtopic
        self.supertopic = supertopic
        self.target = pagename
        self.html = self.buildHTML()
        
    def buildHTML(self):
        callscript = "changeUrl('%s')" %self.target
        html = '<div class="TOCentry" onclick="%s">%s</div>' %(callscript,self.subtopic)
        return(html)

class EntryObject:
    '''class specified attributes of dictionary entry and creates HTML,
    written assuming six columns—-topic, subtopic, headword, 
    definition, soundfile, graphic; soundfile and graphic are optional'''
    def __init__(self, entry):
        memberList = entry.split('\t')
        self.supertopic = memberList[0]
        self.topic = memberList[1]
        self.subtopic = memberList[2].replace('"','')
        self.headword = memberList[3]
        try:
            self.definition = memberList[4].replace('"','')
        except IndexError:
            self.definition = None
        try:
            if len(memberList[5]) != 0:
                self.soundfile = memberList[5]
            else:
                self.soundfile = None
        except IndexError:
            self.soundfile = None
        try:
            if len(memberList[6]) != 0:
                self.graphixfile = memberList[6]
            else:
                self.graphixfile = None
        except IndexError:
            self.graphixfile = None
        self.html = self.buildHtml()
        
    def buildHtml(self):
        '''build the play button'''
        if self.headword == '*SPACE*':
            html = '<div>&nbsp;</div>'
            return(html)
        if self.soundfile:
            path = os.path.dirname(os.path.abspath(__file__))
            pathtoSound = os.path.join(path,'AV/%s' %self.soundfile)
            soundfile = "playSample('%s')" %pathtoSound
            if os.path.isfile(pathtoSound):
                buttonTag = '<button onclick="%s">qwal</button>' %soundfile
            else:
                buttonTag = '<button disabled="True">qwal</button>'
        else:
            buttonTag = '<button disabled="True">qwal</button>'
        '''build img tag'''
        if self.graphixfile:
            path = os.path.dirname(os.path.abspath(__file__))
            pathtoCSS = os.path.join(path,'AV/%s' %self.graphixfile)
            imgTag = '<img class="thumb" src="%s"></img>' %pathtoCSS
        else:
            imgTag = None
        '''make headword and definition tags'''
        headwordTag = '<div class="headword">%s</div>' %self.headword
        defTag = '<div class="definition">%s</div>' %self.definition
        if self.graphixfile:
            '''build HTML for entry with picture'''
            html = '<div class="entryWithGraphics"><div class="stackedEntry">%s %s</div><div class="imageBox">%s</div><div class="buttonColumn"> %s</div></div>' %(headwordTag, defTag, imgTag, buttonTag)    
        else:
            '''build HTML for entry with no picture'''
            html = '<div class="entry">%s %s %s </div>' %(headwordTag, defTag, buttonTag)
        return(html)

def getCSS():
    cssFilename = "childDict.css"
    assert(os.path.exists(cssFilename))
    css = '<link rel = "stylesheet" type = "text/css" href = "%s" />' % cssFilename
    return(css)    

def getJava():
    '''gets the javascript for the main page wireframe (fill iframe)'''
    script2 = '''
function changeUrl(target) {
     document.getElementsByName('wordlists')[0].src = target;
}'''
    scriptTag = "<script>%s</script>" %(script2)
    return(scriptTag)
    
def getSubJava():
    '''gets the javascript for the sub pages (play sound)'''
    script1 = '''
function playSample(audioID) {
    var audio = new Audio(audioID);
    audio.play();
}'''
    scriptTag = "<script>%s</script>" %(script1)
    return(scriptTag)

def makeSubpage(subtopic):
    '''make an .html file for this subtopic;
    input is nestedlist [subtopic,[entry, ...]]'''
    htmlDoc = yattag.Doc()
    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<meta charset="UTF-8">')
            htmlDoc.asis(getSubJava())
            path = os.path.dirname(os.path.abspath(__file__))
            pathtoCSS = os.path.join(path,'childDict.css')
            htmlDoc.asis('<link rel = "stylesheet" type = "text/css" href = "%s" />' %pathtoCSS)
        with htmlDoc.tag('body'):
            with htmlDoc.tag('H1', klass="topic"):
                htmlDoc.text(subtopic[1][0].topic)
            with htmlDoc.tag('H2', klass="subtopic"):
                htmlDoc.text(subtopic[1][0].subtopic)
            for entry in subtopic[1]:
                htmlDoc.asis(entry.html)
    htmlText = htmlDoc.getvalue()
    if subtopic[0][0] != 'Other':
        filename = subtopic[0][0]
    else:
        filename = subtopic[0][0] + subtopic[1][1].topic
    pagename = 'allpages/%s.html' %filename
    with open('%s'%pagename,'w') as f:
        f.write(htmlText)
    '''now make an index object for this subtopic'''
    indexObject = IndexEntry(pagename,subtopic[0][0],subtopic[1][1].topic,subtopic[1][0].supertopic)
    return(indexObject)    

def makeSubtopicPages(objectList):
    '''group entryObjects by subtopic'''
    '''I kind of feel that the two FOR loops could be made into
    one loop, but maybe not today'''
    currentTopic = objectList[0].topic
    currentSubtopic = objectList[0].subtopic
    subtopicList = [[currentSubtopic,currentTopic]] #list of subtopic,topic pairs
    for entry in objectList:
        if entry.topic != currentTopic:
            currentTopic = entry.topic
        if entry.subtopic != currentSubtopic:
            subtopicList.append([entry.subtopic,entry.topic])
            currentSubtopic = entry.subtopic
    '''create nested list [subtopic,[entry, ...]]'''
    nestedList = []
    for subtopic in subtopicList:
        item = [subtopic,[]]
        listofentriesforsubtopic = [entry for entry in objectList if entry.subtopic == subtopic[0] and entry.topic == subtopic[1]]
        item[1] = listofentriesforsubtopic
        nestedList.append(item)
    '''make webpage and index for each subtopic'''
    indexList = []
    for subtopic in nestedList:
        indexObject = makeSubpage(subtopic)
        indexList.append(indexObject)
    return(nestedList,indexList)

def buildNavIndex(indexList):
    currentSupertopic = 'start'
    currentTopic = 'start'
    indexTag = ''
    for index in indexList:
        if index.supertopic != currentSupertopic:
            currentSupertopic = index.supertopic
            indexTag += '<div class="TOCsuperheader">%s</div>' %(currentSupertopic)
        if index.topic != currentTopic:
            currentTopic = index.topic
            indexTag += '<div class="TOCheader">%s</div>' %(currentTopic)
        indexTag += index.html
    return(indexTag)

def makeWireframe(subtopicList, indexList):
    '''build the basic page with the three main divs (container, nav,
    and the dictionary iframe), populate header and call buildIndex method
    to populate nav, which will control the contents of the iframe'''
    htmlDoc = yattag.Doc()
    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<meta charset="UTF-8">')
            htmlDoc.asis(getJava())
            htmlDoc.asis(getCSS())
        with htmlDoc.tag('body'):
            with htmlDoc.tag('div', klass="container"):
                with htmlDoc.tag('div', klass="header"):
                    htmlDoc.text('Hul’q’umi’num Children’s Dictionary')
                with htmlDoc.tag('div', klass="nav"):
                    htmlDoc.asis(buildNavIndex(indexList))
                htmlDoc.asis('<iframe class="dictionary" name="wordlists" src="frontPage.html"></iframe>')
    htmlText = htmlDoc.getvalue()
    return(htmlText)

'''get the command line argument (name of dictionary file)'''
parser = argparse.ArgumentParser()
parser.add_argument('dictFile')
args = parser.parse_args()
dictFile = args.dictFile

'''get the file path to the dictionary file'''
path = os.path.dirname(os.path.abspath(__file__))
pathtofile = os.path.join(path,dictFile)

'''read from dictionary file'''
with open(pathtofile,'r') as dict:
    dictionaryData = dict.read()

'''make text string into list of entries by 
splitting dictionary text string at return (\n) chars'''    
entryList = dictionaryData.split('\n')[1:]
# sortedEntryList = sorted(entryList, key=lambda entryList[0]: (entryList[1](entryList[0]), entryList[0]))

'''create list of entry objects'''
EntryObjectList = []
for entry in entryList:
    if len(entry) <=4:
        continue
    o = EntryObject(entry) 
    EntryObjectList.append(o)
    
'''clean out allpages directory'''
filelist = os.listdir('allpages')
for f in filelist:
    os.remove(os.path.join('allpages', f))
    
'''create HTML file for each subtopic and a list of index entries'''
subtopicList, indexList = makeSubtopicPages(EntryObjectList)

'''make webpage, save file, open in browser'''
page = makeWireframe(subtopicList, indexList)
with open('childDict.html','w') as f:
    f.write(page)
os.system("open %s" %'childDict.html')
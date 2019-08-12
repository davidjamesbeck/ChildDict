import os, argparse
import yattag

class EntryObject:
    '''class specified attributes of dictionary entry and creates HTML,
    written assuming six columns—-topic, subtopic, headword, 
    definition, soundfile, graphic; soundfile and graphic are optional'''
    def __init__(self, entry):
        memberList = entry.split('\t')
        self.topic = memberList[0]
        self.subtopic = memberList[1].replace('"','')
        self.headword = memberList[2]
        self.definition = memberList[3].replace('"','')
        if len(memberList) >= 5 and len(memberList[4]) != 0:
            self.soundfile = memberList[4]
        else:
            self.soundfile = None
        if len(memberList) >= 6 and len(memberList[5]) != 0:
            self.graphixfile = memberList[5]
        else:
            self.graphixfile = None

def makeSubtopicPages(objectList):
    '''group entryObjects by subtopic'''
    '''I kind of feel that the two FOR loops could be made into
    one loop, but maybe not today'''
    currentTopic = objectList[0].topic
    currentSubtopic = objectList[0].subtopic
    subtopicList = [[currentSubtopic,currentTopic]] #list of subtopic names
    for entry in objectList:
                if entry.topic != currentTopic:
                    currentTopic = entry.topic
                if entry.subtopic != currentSubtopic:
                    subtopicList.append([entry.subtopic,entry.topic])
                    currentSubtopic = entry.subtopic
    '''create nested list [subtopic,[entry, ...]]'''
    nestedList = []
    for subtopic in subtopicList:
        item = [subtopic[0],[]]
        listofentriesforsubtopic = [entry for entry in objectList if entry.subtopic == subtopic[0] and entry.topic == subtopic[1]]
        item[1] = listofentriesforsubtopic
##      for entry in objectList:
##          if entry.subtopic == subtopic:
##              item[1].append(entry.headword)
        nestedList.append(item)
    for i,item in enumerate(nestedList):
            print(nestedList[i])

if __name__ == '__main__':
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

    '''create list of entry objects'''
    EntryObjectList = []
    for entry in entryList:
            o = EntryObject(entry) 
            EntryObjectList.append(o)
    makeSubtopicPages(EntryObjectList)

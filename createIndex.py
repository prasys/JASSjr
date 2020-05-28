import sys
import re
from collections import defaultdict
from array import array
import gc


class CreateIndex:

    def __init__(self):
        self.index=defaultdict(list)    #the inverted index


    def getTerms(self, line):
        '''given a stream of text, get the terms from the text''' 
        line=line.lower()
        line=re.sub(r'[^a-z0-9 ]',' ',line) #put spaces instead of non-alphanumeric characters
        line=line.split()
        return line


    def parseCollection(self):
        ''' returns the id, title and text of the next page in the collection '''
        doc=[]
        for line in self.collFile:
            print(line)
            if line=='</DOC>\n':
                break
            doc.append(line)
        
        curPage=''.join(doc) ## current document collection 
        pageid=re.search('<DOCNO>(.*?)</DOCNO>', curPage, re.DOTALL) #parse the primary key/document id where we have found this collection 
        pagetitle=re.search('<IN>(.*?)</IN>', curPage, re.DOTALL) ## TO CHANGE IT TO READ THE TAGS , MIGHT USE BEAUTIFULSOUP to achieve this 
        pagetext=re.search('<TEXT>(.*?)</TEXT>', curPage, re.DOTALL)  ## TO CHANGE IT TO READ THE TAGS , MIGHT USE BEAUTIFULSOUP to achieve this 
        
        if pageid==None or pagetitle==None or pagetext==None:
            return {}

        d={}
        d['id']=pageid.group(1)
        d['title']=pagetitle.group(1)
        d['text']=pagetext.group(1)

        return d


    def writeIndexToFile(self):
        '''write the inverted index to the file'''
        f=open(self.indexFile, 'w')
        for term in self.index.keys():
            postinglist=[]
            for p in self.index[term]:
                docID=p[0]
                positions=p[1]
                postinglist.append(':'.join([str(docID) ,','.join(map(str,positions))]))
            print(''.join((term,'|',';'.join(postinglist))),file=f)
            
        f.close()
        

    def getParams(self):
        '''get the collection file, and the output index file'''
        param=sys.argv
        self.collectionFile=param[1]
        self.indexFile=param[2]
        

    def createIndex(self):
        '''main of the program, creates the index'''
        self.getParams()
        self.collFile=open(self.collectionFile,'r')
        #bug in python garbage collector!
        #appending to list becomes O(N) instead of O(1) as the size grows if gc is enabled.
        gc.disable()
        
        pagedict={}
        pagedict=self.parseCollection()
        #main loop creating the index
        while pagedict != {}:                    
            lines='\n'.join((pagedict['title'],pagedict['text']))
            pageid=str(pagedict['id'])
            terms=self.getTerms(lines)

            
            #build the index for the current page
            termdictPage={}
            for position, term in enumerate(terms):
                try:
                    termdictPage[term][1].append(position)
                except:
                    termdictPage[term]=[pageid, array('I',[position])]
            
            #merge the current page index with the main index
            for termpage, postingpage in termdictPage.items():
                self.index[termpage].append(postingpage)
            
            pagedict=self.parseCollection()


        gc.enable()
            
        self.writeIndexToFile()
        
    
if __name__=="__main__":
    c=CreateIndex()
    c.createIndex()
    


import ciseau
with open('test_documents.xml', 'r') as f: # read the XML file 
    for line in f:
        print(line)
        print(ciseau.tokenize(line))

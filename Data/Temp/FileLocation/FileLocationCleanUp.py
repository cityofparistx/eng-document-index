import os, csv
from collections import defaultdict

directoryDict = {}
directoryDict = defaultdict(lambda:0, directoryDict)

for root, dirs, files in os.walk("Z:\CONSTRUCTION PLANS\FLAT FILES"):
    for file in files:
        #print root
        #print os.path.join(root, file)
        
        rootSplit = root.rsplit("\\", 2)
        index = rootSplit[1] + "-" + rootSplit[2]
        #print index
        
        if file.endswith(".pdf"):
            directoryDict[index] = os.path.join(root, file)

with open('output.csv', 'wb') as output:
    outputWriter = csv.writer(output, delimiter=',')
    
    for key in directoryDict:
        outputWriter.writerow([key, directoryDict[key]])
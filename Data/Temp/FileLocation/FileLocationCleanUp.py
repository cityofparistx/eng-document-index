import os, csv, pyodbc
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

#with open('output.csv', 'wb') as output:
#    outputWriter = csv.writer(output, delimiter=',')
    
#    for key in directoryDict:
#        outputWriter.writerow([key, directoryDict[key]])
     
     
database_location = 'S:\\GIS\\Justin Oliver\\GitHub\\eng-document-index\\Data\\documents.accdb'
connection_string = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;' % database_location

cnxn = pyodbc.connect(connection_string)

cursor = cnxn.cursor()

#cursor.execute("""UPDATE documents SET server_location='test' WHERE physical_index='A-1'""")
for key in directoryDict:
    #sqlStatement = 'UPDATE documents SET server_location="?" WHERE physical_index="?"', str(key), os.path.join(directoryDict[key])
    #print sqlStatement
    print str(key)
    cursor.execute("""UPDATE documents SET server_location='{0}' WHERE physical_index='{1}'""".format(os.path.join(directoryDict[key]), str(key)))
    #print 'UPDATE documents SET server_location="' + str(key) + '" WHERE physical_index="' + str(directoryDict[key] + '"')

cnxn.commit()
cnxn.close()
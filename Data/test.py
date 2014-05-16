import pyodbc
import pystache

database_location = 'S:\\GIS\\Justin Oliver\\GitHub\\eng-document-index\\Data\\documents.accdb'
connection_string = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;' % database_location

cnxn = pyodbc.connect(connection_string)
cursor = cnxn.cursor()

#sqlStatement = 'SELECT documents.doc_name, documents.doc_date, documents.physical_index FROM doc_tag_relation INNER JOIN documents ON documents.doc_id = doc_tag_relation.doc_id WHERE doc_tag_relation.tag_id=41;'

sqlStatement = 'SELECT * FROM tags;'
cursor.execute(sqlStatement)
tag_rows = cursor.fetchall()

for tag in tag_rows:
    sqlStatement = 'SELECT documents.doc_name, documents.doc_date, documents.physical_index FROM doc_tag_relation INNER JOIN documents ON documents.doc_id = doc_tag_relation.doc_id WHERE doc_tag_relation.tag_id=' + str(tag.tag_id)
    docs = cursor.execute(sqlStatement)
    print tag.tag_name
    for doc in docs:
        print doc
    
cnxn.close()
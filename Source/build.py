import pyodbc
import pystache

database_location = 'S:\\GIS\\Justin Oliver\\GitHub\\eng-document-index\\Data\\documents.accdb'
connection_string = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;' % database_location

cnxn = pyodbc.connect(connection_string)
cursor = cnxn.cursor()

#sqlStatement = 'SELECT documents.doc_name, documents.doc_date, documents.physical_index FROM doc_tag_relation INNER JOIN documents ON documents.doc_id = doc_tag_relation.doc_id WHERE doc_tag_relation.tag_id=41;'

sqlStatement = 'SELECT * FROM tags ORDER BY tag_type DESC, tag_name;'
cursor.execute(sqlStatement)
tag_rows = cursor.fetchall()

with open('..\\Build\\index.htm', 'wb') as mainIndex:
    current_tag_type = ""
    mainIndex.write('<a href="index.htm">Home</a><br>\n')
    for tag in tag_rows:
        sqlStatement = 'SELECT doc_tag_relation.location_desc, documents.doc_date, documents.physical_index FROM doc_tag_relation INNER JOIN documents ON documents.doc_id = doc_tag_relation.doc_id WHERE doc_tag_relation.tag_id=' + str(tag.tag_id)
        docs = cursor.execute(sqlStatement)
        scrubbedTagName = tag.tag_name.replace('/', '-')
        
        #print tag.tag_name
        
        if tag.tag_type != current_tag_type:
            mainIndex.write('<h2>' + tag.tag_type + '</h2>\n')
        
        current_tag_type = tag.tag_type
        mainIndex.write('<a href="Tags\\' + scrubbedTagName + '.htm">' + tag.tag_name + '</a><br>\n')
        
        with open('..\\Build\\Tags\\' + scrubbedTagName + '.htm', 'wb') as tagFile:
            tagFile.write('<a href="..\index.htm">Home</a><br>\n')
            tagFile.write('<h2>' + tag.tag_name + '</h2>\n')
            tagFile.write('<table>\n')
            tagFile.write('<tr><td>Index</td><td>Date</td><td>Location</td></tr>\n')
            for doc in docs:
                documentDate = ''
                if doc.doc_date:
                    documentDate = doc.doc_date.strftime('%Y-%m-%d')
                    
                tagFile.write('<tr><td>' + str(doc.physical_index) + '</td><td>' + documentDate + '</td><td>' + str(doc.location_desc) + '</td></tr>\n')
                
            tagFile.write('</table>\n')
cnxn.close()
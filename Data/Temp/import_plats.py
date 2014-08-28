import pyodbc, os

database_location = 'S:\\GIS\\Justin Oliver\\GitHub\\eng-document-index\\Data\\documents.accdb'
connection_string = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;' % database_location

cnxn = pyodbc.connect(connection_string)

cursor = cnxn.cursor()


for root, dirs, files in os.walk(r"Z:\CITY PLATS\Supplemental"):
        for file in files:
            doc_name = file
            subdivision = root.rsplit("\\", 1)[1]
            server_location = os.path.join(root, file)
            doc_type = "Plat Supplement"
            
            sqlStatement = """INSERT INTO plats(doc_name, server_location, subdivision, doc_type) VALUES ('{0}', '{1}', '{2}', '{3}')""".format(doc_name, server_location, subdivision, doc_type)
            print sqlStatement
            cursor.execute(sqlStatement)
            

cnxn.commit()
cnxn.close()
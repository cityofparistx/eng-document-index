import pyodbc, json
from pystache import Renderer

renderer = Renderer()

index_template = 'Templates\\index.mustache'
tag_index_page_template = 'Templates\\tag_index_page.mustache'

root = '..\\Build\\web\\'


def main():

    tag_rows = loadTags()
    index_data = { 'type': [] }
    json_tag_data = { 'tags': [] }
    
    current_tag_type = ""
    current_tag_type_index = -1

    
    for tag in tag_rows:
        #safe_tage_name is used to remove foreign characters out of tag name for directory creation
        safe_tag_name = tag.tag_name.replace('/', '-')
        
        #tracks if the tag type changes (tag data is loaded sorted by tag_type and the tag_name)
        #If new tag_type is detected than a new type section is created for rendering
        if tag.tag_type != current_tag_type:
            index_data['type'].append(createTypeSection(tag.tag_type))
            current_tag_type = tag.tag_type
            current_tag_type_index = current_tag_type_index + 1
            
        index_data['type'][current_tag_type_index]['tags'].append(createTagSection(tag.tag_name, safe_tag_name))
        json_tag_data['tags'].append(createTagJsonData(tag.tag_name, safe_tag_name))
                
        createTagPage(tag.tag_id, tag.tag_name, safe_tag_name)
        
    createTagJson(json_tag_data)
    createIndex(index_data)


# Functions to create proper dictionary & list formats for mustache templates
# Remember sections == lists & variables == dictionaries
def createTypeSection(str):
    return { 'tag_type': str, 'tags': [] }
    
def createTagSection(tag_name, safe_tag_name):
    return { 'tag_name': tag_name, 'safe_tag_name': safe_tag_name }

def createTagJsonData(tag_name, safe_tag_name):
    return { 'tag_name': tag_name, 'location': safe_tag_name + '.htm' }

def createTagJson(data):
    with open(root + 'dist\\search.json', 'wb') as JSON:
        JSON.write(json.dumps(data))
    
# Functions to render html pages based on mustache templates and tag data
def createIndex(data):
    with open(index_template, 'r') as template:
                
        with open(root + 'index.htm', 'wb') as mainIndex:
            mainIndex.write(renderer.render(template.read(), data))

def createTagPage(tag_id, tag_name, safe_tag_name):
    with open(tag_index_page_template, 'r') as template:

        data = getTagPageData(tag_id, tag_name)

        with open( root + safe_tag_name + '.htm', 'wb') as tagPage:
            tagPage.write(renderer.render(template.read(), data))

            
# Formats tag data from database for mustache rendering 
def getTagPageData(tag_id, tag_name):
    docs = loadDocumentsByTag(tag_id)
    
    doc_data = { 'tag_name': tag_name, 'table': [] }
    document_date = ''

    for doc in docs:
        #loop through all documents and add create data for mustache template renderer
        if doc.doc_date:
            #if date is present reformat into string. If Null do nothing and leave docuement_date as empty string
            document_date = doc.doc_date.strftime('%Y-%m-%d')
            
        doc_data['table'].append({'physical_index': doc.physical_index, 'tag_date' : document_date, 'location_desc': doc.location_desc })

    return doc_data

# Simple data access layers
def loadTags():
    sqlStatement = 'SELECT * FROM tags ORDER BY tag_type DESC, tag_name;'
    return loadSqlStatement(sqlStatement)
    
def loadDocumentsByTag(tag_id):
    sqlStatement = 'SELECT doc_tag_relation.location_desc, documents.doc_date, documents.physical_index FROM doc_tag_relation INNER JOIN documents ON documents.doc_id = doc_tag_relation.doc_id WHERE doc_tag_relation.tag_id=' + str(tag_id)
    return loadSqlStatement(sqlStatement)
    
def loadSqlStatement(sqlStatement):
    database_location = 'S:\\GIS\\Justin Oliver\\GitHub\\eng-document-index\\Data\\documents.accdb'
    connection_string = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;' % database_location

    cnxn = pyodbc.connect(connection_string)
    
    cursor = cnxn.cursor()
    cursor.execute(sqlStatement)
    data = cursor.fetchall()
    
    cnxn.close()
    
    return data

main()
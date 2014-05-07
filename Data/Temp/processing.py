import csv

document_dictionary = {}
tag_dictionary = {}

#Load the document data, add the physical id ("C-27") and doc_id (integer) to a dictionary for lookup below
with open("documents.csv") as document_input:
    document_reader = csv.reader(document_input, delimiter=',', quotechar='"')
    next(document_reader, None)
    for row in document_reader:
        document_dictionary[row[5]] = row[0]

#Load the tag data from construction plans, add the tag_original ("Waterplant", "10th NE") and tag_id (integer) to a dictionary for lookup below        
with open("tags.csv") as tag_input:
    tag_reader = csv.reader(tag_input, delimiter=',', quotechar='"')
    next(tag_reader, None)
    for row in tag_reader:
        tag_dictionary[row[0]] = row[4]
        
#print "A-10 doc_id is: " + document_dictionary["A-10"]
#print "10th NE tag_id is: " + tag_dictionary["10th NE"]

#open the doc_tag_relation and add corresponding id numbers from document and tag data above
#If the tag or document in the data exists, the id number is added to the row when rewriting the new output file
with open("doc_tag_relation.csv") as doc_tag_input:
    doc_tag_reader = csv.reader(doc_tag_input, delimiter=',', quotechar='"')
    next(doc_tag_reader, None)
    
    with open("output/doc_tag_relation.csv", "wb") as output:
        outputwriter = csv.writer(output, delimiter=',', quotechar='"')
        outputwriter.writerow(['doc_code', 'tag_note', 'tag_name', 'doc_id', 'tag_id'])
        
        for row in doc_tag_reader:
            outputwriter.writerow([row[0], row[1], row[2], document_dictionary.get(row[0], None), tag_dictionary.get(row[2], None)])
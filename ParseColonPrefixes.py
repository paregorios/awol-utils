import glob
import xml.etree.ElementTree as xmlParser

uniqueTagList = []
# Gets the list of all the *-atom.xmls from the awol-backup directory
atomXMLsPath = 'D:\\GitHub\\awol-backup\\'
xmlList = glob.glob(atomXMLsPath + '*-atom.xml')
#Loop through the list of xmls
for item in xmlList:
    doc=xmlParser.parse(item) #Parse each of the atom.xml
    root = doc.getroot()            
    try:
        titleText = str(root.find("{http://www.w3.org/2005/Atom}title").text) #Get the text from the title element
        # If the title text contains ':', fetch the string before ':'
        if ":" in titleText:
            tag = titleText.split(':')[0]
            print 'SUCCESS-- '+ tag + ' - taken from - ' + '\"'+titleText+'\"'
            if not uniqueTagList.__contains__(tag):
                uniqueTagList.append(tag)
    except UnicodeEncodeError, e:
        print '******ERROR******'
        print e
        print '*****************'
print '******UNIQUE LIST******'
for item in uniqueTagList:
    print 'Item: '+ item

import argparse
import glob
import logging as l
import os
import sys
import traceback
import xml.etree.ElementTree as xmlParser
import codecs

SCRIPT_DESC = 'parse unique colon-delimited prefixes out of Ancient World Online blog XML dump files (Atom format)'
DEFAULTINPATH='D:\\GitHub\\awol-backup\\'
DEFAULTOUTPATH='.\\parse.log'

def main():
    """ 
    main function: parse colon prefixes out of the awol xml dump files
    """

    global args
    if args.outpath:
        DEFAULTOUTPATH = args.outpath
    if args.verbose:
        l.basicConfig(filename=DEFAULTOUTPATH, level=l.DEBUG)
    else:
        l.basicConfig(filename=DEFAULTOUTPATH, level=l.INFO)

    uniqueTagList = []
    tagListFile = codecs.open(DEFAULTOUTPATH, 'a', 'utf-8')
    # Gets the list of all the *-atom.xmls from the awol-backup directory
    atomXMLsPath = args.inpath
    xmlList = glob.glob(atomXMLsPath + '*-atom.xml')
    #Loop through the list of xmls
    for item in xmlList:
        l.debug("trying to parse %s" % item)
        doc=xmlParser.parse(item) #Parse each of the atom.xml
        root = doc.getroot()            
        try:
            l.debug("trying to get text content of the 'title' element")
            titleText = unicode(root.find("{http://www.w3.org/2005/Atom}title").text) #Get the text from the title element
        except UnicodeEncodeError, e:
            l.debug("******ERROR******")
            l.debug(e)
            l.debug("*****************")
        else:
            # If the title text contains ':', fetch the string before ':'
            if ":" in titleText:
                l.debug("   found ':' in title content; trying to split")
                tag = titleText.split(':')[0]
                l.info("SUCCESS-- %s - taken from - \"%s\"" % (tag, titleText))
                if not uniqueTagList.__contains__(tag):
                    uniqueTagList.append(tag)
    for uniqueTag in uniqueTagList:
        tagListFile.write(unicode(uniqueTag))
        tagListFile.write("\n")

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description=SCRIPT_DESC, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument ("-v", "--verbose", action="store_true", help="verbose output (i.e., debug logging")
        parser.add_argument ("-i", "--input",dest="inpath",type=str,default=DEFAULTINPATH,help='input path (directory)')
        parser.add_argument ("-o", "--output",dest="outpath",type=str,default=DEFAULTOUTPATH,help='output path (directory)')
        args = parser.parse_args()
        main()
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        l.debug("ERROR, UNEXPECTED EXCEPTION")
        l.debug(e)
        traceback.print_exc()
        os._exit(1)

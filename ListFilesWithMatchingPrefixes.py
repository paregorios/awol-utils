#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from collections import Counter
import glob
import logging as l
import os
import re
import sys
import traceback
import xml.etree.ElementTree as xmlParser
import codecs

SCRIPT_DESC = 'list all AWOL dump files with prefixes matching a predefined list'

here = os.path.dirname(__file__)

DEFAULTINPATH='D:\\GitHub\\awol-backup\\'
DEFAULTPREFIXESPATH=os.path.join(here, 'text-mining', 'awol-trigger-strings-include-singles.txt')
DEFAULTOUTPATH=os.path.join(here, 'list.log')

def main():
    """ 
    main function: parse colon prefixes out of the awol xml dump files
    """

    global args
    if args.verbose:
        l.basicConfig(level=l.DEBUG)
    else:
        l.basicConfig(level=l.INFO)

    rxcolonchomp = re.compile(u'^\s*:\s*')

    f = codecs.open(args.prefixpath, 'r', 'utf-8')
    prefixes = f.readlines()
    f.close()
    prefixes = [p.strip() for p in prefixes]
    l.debug(prefixes)

    fileListFile = codecs.open(args.outpath, 'a', 'utf-8')
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
            titleText = unicode(root.find("{http://www.w3.org/2005/Atom}title").text).strip() #Get the text from the title element
        except UnicodeEncodeError, e:
            l.debug("******ERROR******")
            l.debug(e)
            l.debug("*****************")
        else:
            l.debug('titleText: %s' % titleText)
            for p in prefixes:
                #l.debug('    testing for prefix: %s' % p)
                if titleText.startswith(p):
                    l.debug('    FOUND!')
                    shortTitle = titleText[len(p):].strip()
                    shortTitle = rxcolonchomp.sub(u'', shortTitle).strip()
                    l.debug("before: '%s'\t\t\nafter: '%s'" % (titleText, shortTitle))
                    titleText = shortTitle
                    fileListFile.write(u"%s\n" % os.path.split(item)[-1])
                    break


#    titleWords = [w.lower() for w in titleWords]
#    c=Counter(titleWords)
#    for uniqueWord in sorted(c.keys()):
#        wordListFile.write(u"%s,%s\n" % (unicode(uniqueWord), c[uniqueWord]))

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description=SCRIPT_DESC, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument ("-v", "--verbose", action="store_true", help="verbose output (i.e., debug logging")
        parser.add_argument ("-i", "--input",dest="inpath",type=str,default=DEFAULTINPATH,help='input path (directory)')
        parser.add_argument ("-p", "--prefixes",dest="prefixpath",type=str,default=DEFAULTPREFIXESPATH,help='path to prefixes text file')
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

#!/usr/bin/env python

# Search replace file with check.

import os, sys, glob
import multi_replace
import file_morpher
from Tkinter import *
import tkMessageBox

class IterLines:
    def __init__(self, filename):
        self.filename = filename
        self.ifs = open(self.filename)
        self.line = ""
        
    def __iter__(self):
        return self
    
    def next(self):
        while 1:
            self.line = self.ifs.readline()
            if len(self.line) == 0: raise StopIteration # end of file
            if self.line[0] == '#': continue # skip lines that start with a comment
            self.line = self.line[:-1] # trim off \r\n
            break
        return self.line
    
class RepFiles:
    usage = "usage: %s -[tu] [infofile]" % os.path.basename(sys.argv[0])
    usage += """
    -t for test
    -u for update (can't have -t and -u at the same time)
    if info file is missing 'replacer.replacer' is assumed"""
    
    def __init__(self):
        self.dict = {}
        self.op = ''
        self.filename = ''
        
    def getParms(self):
        if len(sys.argv) < 2:
            print RepFiles.usage
            sys.exit(-1)
        self.opt = sys.argv[1]
        if self.opt not in ['-t', '-u']:
            print "Invalid parameter:", self.opt
            print usage
            sys.exit(0)
    
        if (len(sys.argv) >= 2):
            self.filename = sys.argv[2]
        else:
            self.filename = "replacer.replacer"
        
        try:
            os.stat(self.filename)
        except:
            print "File:", self.filename, "not found"
            sys.exit(-1)
            
        if self.opt == '-u':
            if not tkMessageBox.askyesno("Sure?", "Do you want to replace all the files?"):
                sys.exit(-1)
            
    def exit(self):
        print "Quitting"
        sys.exit(-1)
        
    def readDatFile(self):
        infile = IterLines(self.filename)
        
        self.path = infile.next()
            
        self.dict = {}
        strFrom = ""
        strTo = ""
        while 1:
            try:
                line = infile.next()
            except StopIteration:
                break
            
            if len(strFrom) == 0:
                strFrom = line # remove \r\n
            else:
                strTo = line
                self.dict[strFrom] = strTo
                strFrom = ""
                strTo = ""
    
        if self.opt == "-t":
            for (key, val) in self.dict.iteritems():
                self.dict[key] = "[" + val + "]"
        
    def doIt(self):
        self.getParms()
        self.readDatFile()
        rep = multi_replace.multi_replace(self.dict)
        rep.compile()
        
        nFileCount = 0
        nTotFileCount = 0
        for file in glob.glob(self.path):
            (root, ext)= os.path.splitext(file)
            
            if ext.lower() == ".replacer": 
                print "Skipping:", file
                continue  # skip if .replacer
            
            nTotFileCount += 1
            
            if self.opt == '-u':
                fm = file_morpher.FileMorpher(file)
                out = fm.opentemp()
                
            input = open(file)
            nDiff = 0
            nLineCount = 0

            for s in input.xreadlines():
                diff = rep.sub(s)
                nLineCount += 1
    
                if self.opt == '-u':
                    out.write(diff)
                    
                if diff != s:
                    if nDiff == 0:
                        nFileCount += 1
                    nDiff += 1
                    
                    print "  File \"%s\", line %d" % (file, nLineCount)
                    print "\t%s" % (diff,)
    
            input.close()
            if self.opt == '-u':
                if nDiff > 0:
                    fm.commit()
                else:
                    fm.rollback()
                
        print "Found %d/%d files to change" % (nFileCount, nTotFileCount)

if __name__ == "__main__":
    rep = RepFiles()
    rep.doIt()

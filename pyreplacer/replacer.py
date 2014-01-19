#!/usr/bin/env python

"""Search replace file with check."""

import file_morpher
import fnmatch
import glob
import multi_replace
import optparse
import os
import sys
import yaml

def query_yes_no(question, default=None):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default is None:
        prompt = " [y/n] "
    elif default:
        prompt = " [Y/n] "
    else:
        prompt = " [y/N] "

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

class RepFiles:
    usage = "usage: %s -[tu] [infofile]" % os.path.basename(sys.argv[0])
    usage += """
    -u for update
    if info file is missing 'replacer.replacer' is assumed"""

    def __init__(self):
        self.config = {}
        self.op = ''
        self.replacer_filename = ''
        self.rep = None

    def getParms(self):
        parser = optparse.OptionParser(usage=RepFiles.usage,
                                       version="%prog 1.0")
        parser.add_option("-u", "--update", dest="update", action="store_true",
                          default=False, help="Update the files.")
        (self.options, args) = parser.parse_args()
        if args:
            self.replacer_filename = args[0]
        else:
            self.replacer_filename = "replacer.replacer"
        try:
            os.stat(self.replacer_filename)
        except:
            print "File:", self.replacer_filename, "not found"
            sys.exit(-1)

        if self.options.update:
            if (not query_yes_no('Do you want to replace all the files?',
                                 default=False)):
                sys.exit(-1)

    def exit(self):
        print 'Quitting'
        sys.exit(-1)

    def readDatFile(self):
        self.config = yaml.load(open(self.replacer_filename))

    def one_dir(self, path):
        pathpart, globpart = os.path.split(path)
        for (dirpath, dirnames, filenames) in os.walk(pathpart):
            for filename in filenames:
              if not fnmatch.fnmatch(filename, globpart):
                continue
              fullpath = os.path.join(dirpath, filename)
              (root, ext)= os.path.splitext(fullpath)
              if ext.lower() == '.replacer':
                  print 'Skipping:', fullpath
                  continue  # skip if .replacer

              self.replace_one_file(fullpath)

    def doIt(self):
        self.getParms()
        self.readDatFile()
        self.rep = multi_replace.MultiReplace(self.config)
        self.rep.compile()

        nFileCount = 0
        nTotFileCount = 0
        for path in self.config['path']:
            self.one_dir(path)

    def replace_one_file(self, fullpath):
        if self.options.update:
            fm = file_morpher.FileMorpher(fullpath)
            out = fm.opentemp()

        input = open(fullpath)
        nDiff = 0
        line_no = 0

        for s in input.xreadlines():
            diff = self.rep.sub(s)
            line_no += 1

            if self.options.update:
                out.write(diff)

            if diff != s:
                nDiff += 1

                print '  File \'%s\', line %d' % (fullpath, line_no)
                print '\t%s' % (diff,)

        input.close()
        if self.options.update:
            if nDiff > 0:
                fm.commit()
            else:
                fm.rollback()
        return nDiff


if __name__ == '__main__':
    rep = RepFiles()
    rep.doIt()

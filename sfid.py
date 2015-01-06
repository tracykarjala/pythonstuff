
__author__ = 'tracykarjala'
#!/usr/bin/python

import os
import argparse
import sys

parser = argparse.ArgumentParser(description='Searches all files in a directory for a string.')
parser.add_argument('-i', '--inputdir', default=os.getcwd(), help='Directory to search. If a directory is not specified\
                        the current working directory is searched.', required=False)
parser.add_argument('-o', '--outputfile', help='Output file name. If full path to file is not provided file is created \
                        in current working directory.', required=True)
parser.add_argument('-s', '--searchstring', nargs='*', help='The string (or multiple strings) to search for in all \
                        files.  If the strings you are searching for contain spaces surround each string parameter \
                        in double quotes.', required=True)
parser.add_argument('-f', '--file', help='Logs each file name that is opened to output file to identify what file each \
                        occurrence of the string is located in. Also puts line number in the source file for each \
                        instance of the string in the output file.', action="store_true", required=False)
# if no arguments are provided to the program print help
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

try:
    d = open(args.outputfile, 'w')
    print 'Searching for strings %s in "%s"' % (args.searchstring, args.inputdir)
    d.write('Search for strings' + str(args.searchstring) + '\n')
    for filename in os.listdir(args.inputdir):
        #skip subdirectories
        if os.path.isdir(os.path.join(args.inputdir, filename)):
            continue
        # make sure we don't search the output file, as this causes a loop that chews up disk space
        if not filename == args.outputfile:
            try:
                filepath = os.path.join(args.inputdir, filename)
                f = open(filepath, 'r')
                linenum = 0
                if args.file:
                    d.write('\n' + filename + '\n')
                for line in f:
                    linenum += 1
                    for s in args.searchstring:
                        if s in line:
                            if args.file:
                                d.write(str(linenum) + ': ' + line)
                            else:
                                d.write(line)
                f.close()
            # skip any file we can't open due to permissions issues, file locks, etc
            except IOError:
                print "Error opening %s. Continuing." % filename
    d.close()
#  can't open output file due to permissions issues, file locks, etc
except IOError:
    print 'Error opening outputfile %s.' % args.outputfile

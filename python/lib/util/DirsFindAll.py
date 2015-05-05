#!/usr/bin/python
# encoding: utf-8
""" DirsFindAll.py

Find all directories with specified regular expression 'pattern' starting at the
given 'root' directory.  Specify 'singleLevel = True' to void traversing 
of subdirectories.
 
"""
import os
from fnmatch import fnmatch
def DirsFindAll(root, patterns='*', singleLevel=False):
    """ Given root directory, find all files with requested patterns """
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        
        for name in subdirs:
            for pattern in patterns:
                if fnmatch(name,pattern):
                    yield os.path.join(path,name)
                    break
        if singleLevel :
            break

if __name__ == '__main__':
    import sys
    argc = len(sys.argv)
    if argc > 3:
        DirsFindAll(sys.argv[1], sys.argv[2], sys.argv[3])
    elif argc == 3:
        DirsFindAll(sys.argv[1], sys.argv[2])
    elif argc == 2:
        DirsFindAll(sys.argv[1])
    else:
        print('Provide at least the root directory')

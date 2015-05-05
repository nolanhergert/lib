#!/usr/bin/python
# encoding: utf-8
""" FilesFind.py

Find files with specified 'pattern' in a list of directories specified
by 'searchPath'. Use the appropriate OS path separator.

"""
import os, glob
def FilesFind(searchPath, pattern, pathsep=os.pathsep):
    """ Given searchPath, find files with requested pattern """
    for path in searchPath.split(pathsep):
        for match in glob.glob(os.path.join(path,pattern)):
            yield match

if __name__ == '__main__':
    import sys
    argc = len(sys.argv)
    if argc > 2:
        for match in FilesFind(sys.argv[1], sys.argv[2]):
            print(match)
    else:
        print('Usage: FilesFind(searchPath, pattern, pathsep=os.pathsep) - ')
        print('   Provide the searchpath string or list of directories ' )
        print('   separated by pathsep and the regular expression pattern to ')
        print('   describe the files to find.')

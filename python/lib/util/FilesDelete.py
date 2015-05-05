#!/usr/bin/python
# encoding: utf-8
"""FilesDelete.py

Delete the files starting in the 'rootdir' with the specified 'patterns'.

"""
import os
from FilesFindAll import FilesFindAll
def FilesDelete(rootDir, patterns, pathsep=os.pathsep):
    
    for dataFile in FilesFindAll(rootDir, patterns, pathsep):
        os.system('del' + ' ' + '\"'+dataFile+'\"')
       
if __name__ == '__main__':
    import sys
    argc = len(sys.argv)
    if argc > 2:
        ans = raw_input('Be very careful! Are you sure? If so, type "yes"')
        if(ans == 'yes'):
            FilesDelete(sys.argv[1], sys.argv[2])    
    else:
        print('Usage: FilesDelete(rootDir, patterns, pathsep=os.pathsep) - ')
        print('   Delete the files starting in the rootdir ' )
        print('   with the specified patterns ')
        

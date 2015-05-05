#!/usr/bin/python
# encoding: utf-8
""" FilesFindAll.py

Find all files with specified regular expression 'pattern' starting at the
given 'root' directory.  Specify 'singleLevel = True' to void traversing
of subdirectories and specify 'yieldFolders = True' to also return folder names.
Specify subDirectoryPattern to be a specific subdirectory pattern you want the
files to be contained inside. Ex: Vigileo_A* as opposed to Vigileo_B*

"""
from fnmatch import fnmatch
from python.lib.util.SortNatural_Key import SortNatural_Key
import os
def FilesFindAll(root, patterns = '*', singleLevel = False, \
                 yieldFolders = False, parentDirectoryPatterns = '*'):
    """ Given root directory, find all files with requested patterns """
    patterns = patterns.split(';')
    parentDirectoryPatterns = parentDirectoryPatterns.split(';')
    for path, subdirs, files in os.walk(root, topdown = True):
        
        # Don't include files that don't correspond to parentDirectoryPatterns
        if (parentDirectoryPatterns[0] != '*'):
            parent = os.path.basename(path)
            # All patterns need to not match in order to skip this directory
            matches = [(fnmatch(parent,p)) for p in parentDirectoryPatterns]
            if (any(matches)):
                # Return the files
                pass
            else:
                # Continue on to any subdirectories
                continue
        
        if yieldFolders:
            files.extend(subdirs)
        
           
        # Use natural sorting to sort files
        files.sort(key = SortNatural_Key)
        for name in files:
            for pattern in patterns:
                if fnmatch(name, pattern):
                    yield os.path.join(path, name)
                    break
        if singleLevel :
            break

if __name__ == '__main__':
    
    files = [(f) for f in FilesFindAll(r'..\biomed\ewdb\test\MIM08010011', patterns = '*.PCO', parentDirectoryPatterns = 'Vigileo_B*')]
    assert len(files) == 8, 'It doesn''t work...'
    print files
        
    import sys
    argc = len(sys.argv)
    if argc > 4:
        FilesFindAll(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    elif argc == 4:
        FilesFindAll(sys.argv[1], sys.argv[2], sys.argv[3])
    elif argc == 3:
        FilesFindAll(sys.argv[1], sys.argv[2])
    elif argc == 2:
        FilesFindAll(sys.argv[1])
    else:
        print('Provide at least the root directory')

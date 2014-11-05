#!/usr/bin/env python3
# Copyright (C) 2013-2014 Karl R. Wurst
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA

###################################################################
# Cleans up assignment files downloaded from Blackboard's gradebook
# by deleting all .txt files with no student text data or comments
# and renaming all the remaining files to username-studentfilename.ext

# Call as:
# python bbcleanup.py directory

import sys
import os
import os.path

def bbcleanup():
    os.chdir(sys.argv[1])
    
    deleteContentFreeTextFiles(filterForFilesOnly(os.listdir()))    
    unmungeAndRenameBlackboardFiles(filterForFilesOnly(os.listdir()))

def unmungeAndRenameBlackboardFiles(fileNameList):
    unmungedFileNameList = unmungeBlackboardFileNames(fileNameList)
    renameList = zip(fileNameList, unmungedFileNameList)
    for pair in renameList:
        os.rename(pair[0], pair[1])
     
def deleteContentFreeTextFiles(filenameList):   
    deleteList = filterForContentFreeTextFiles(filenameList)
    for f in deleteList:
        os.remove(f)

def unmungeBlackboardFileNames(filenameList):
    returnList = []
    for f in filenameList:
        if '_attempt_' in f:
            f = removeSpacesAndParentheses(f)   
            if isTextFile(f):
                first = f.find('_')  # location of first underscore
                second = f.find('_', first + 1)  # location of second underscore
                newf = f[first + 1:second] + '.txt'
                returnList.append(newf)
            else:
                first = f.find('_')  # location of first underscore
                second = f.find('_', first + 1)  # location of second underscore
                last = f.rfind('_')  # location of last underscore
                newf = f[first + 1:second] + '-' + f[last + 1:]
                returnList.append(newf)
    return returnList
 
def filterForContentFreeTextFiles(filenameList):
    returnList = []
    for f in filenameList:
        if '_attempt' in f and isTextFile(f):
            with open(f) as file:
                contents = file.read()
            if 'There are no student comments for this assignment' in contents and \
               'There is no student submission text data for this assignment.' in contents:
                returnList.append(f)
    return returnList
    
def isTextFile(filename):
    return '.txt' == filename[-4:]

def filterForFilesOnly(directoryContentsList):
    return [ f for f in directoryContentsList if os.path.isfile(f) ]

def removeSpacesAndParentheses(string):
    return string.replace(' ', '').replace('(', '').replace(')', '')
            
if __name__ == '__main__':
    bbcleanup()

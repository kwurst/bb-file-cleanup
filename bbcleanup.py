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

#######################################################################
# Cleans up assignment files downloaded from Blackboard's gradebook by:
#  - deleting all .txt files with no student text data or comments
#  - renaming remaining .txt files to username.txt
# -  renaming all other files to username-userfilename.ext

# Call as:
# python bbcleanup.py working-directory

import sys
import os
import os.path

def bbcleanup():
    changeToWorkingDirectory()
    deleteContentFreeTextFiles(filterForAttemptFiles(os.listdir()))    
    unmungeAndRenameBlackboardFiles(filterForAttemptFiles(os.listdir()))

def deleteContentFreeTextFiles(filenameList):   
    deleteList = filterForContentFreeTextFiles(filenameList)
    for filename in deleteList:
        os.remove(filename)

def unmungeAndRenameBlackboardFiles(fileNameList):
    unmungedFileNameList = unmungeBlackboardFilenames(fileNameList)
    renameList = zip(fileNameList, unmungedFileNameList)
    for pair in renameList:
        os.rename(pair[0], pair[1])
     
def filterForContentFreeTextFiles(filenameList):
    return [f for f in filenameList if isContentFreeTextFile(f)]

def unmungeBlackboardFilenames(filenameList):
    return [unmungeSingleBlackboardFilename(f) for f in filenameList if isAttemptFile(f)]
 
def unmungeSingleBlackboardFilename(filename):
    filename = removeSpacesAndParentheses(filename)
    username = getUsername(filename)
    submittedFilename = getSubmittedFilename(filename)
    return username + submittedFilename

def isContentFreeTextFile(filename):
    if isTextFile(filename):
        contents = getFileContents(filename)
        if 'There are no student comments for this assignment' in contents and \
            'There is no student submission text data for this assignment.' in contents:  
            return filename
              
def isTextFile(filename):
    return '.txt' == filename[-4:]

def getFileContents(filename):
    with open(filename) as file:
        return file.read()

def filterForAttemptFiles(directoryContentsList):
    return [ f for f in directoryContentsList if os.path.isfile(f) and isAttemptFile(f) ]

def isAttemptFile(filename):
    return '_attempt_' in filename

def removeSpacesAndParentheses(string):
    return string.replace(' ', '').replace('(', '').replace(')', '')

def getUsername(filename):
    firstUnderscore = filename.find('_')
    secondUnderscore = filename.find('_', firstUnderscore + 1)
    return filename[firstUnderscore + 1:secondUnderscore]

def getSubmittedFilename(filename):
    if isTextFile(filename):
        return '.txt'
    else:
        lastUnderscore = filename.rfind('_')
        return '-' + filename[lastUnderscore + 1:]

def changeToWorkingDirectory():
    os.chdir(sys.argv[1]) 
        
if __name__ == '__main__':
    bbcleanup()

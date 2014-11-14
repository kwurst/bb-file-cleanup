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
import re

def bbcleanup():
    changeToWorkingDirectory()
    deleteContentFreeBlackboardGeneratedFiles(getAttemptFiles())    
    renameBlackboardFiles(getAttemptFiles())

def deleteContentFreeBlackboardGeneratedFiles(filenameList):   
    deleteList = filterForContentFreeBlackboardGeneratedFiles(filenameList)
    for filename in deleteList:
        os.remove(filename)

def renameBlackboardFiles(filenameList):
    for filename in filenameList:
        os.rename(filename, fixBlackboardFilename(filename))
     
def filterForContentFreeBlackboardGeneratedFiles(filenameList):
    return [f for f in filenameList if isContentFreeBlackboardGeneratedFile(f)]

def fixBlackboardFilename(filename):
    filename = removeSpacesAndParentheses(filename)
    username = getUsername(filename)
    submittedFilename = getSubmittedFilename(filename)
    return username + submittedFilename

def isContentFreeBlackboardGeneratedFile(filename):
    if isBlackboardGeneratedFile(filename):
        contents = getFileContents(filename)
        if 'There are no student comments for this assignment' in contents and \
            'There is no student submission text data for this assignment.' in contents:  
            return filename
              
def getFileContents(filename):
    with open(filename) as file:
        return file.read()

def getAttemptFiles():
    return filterForAttemptFiles(os.listdir())
    
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
    if isBlackboardGeneratedFile(filename):
        return '.txt'
    else:
        lastUnderscore = filename.rfind('_')
        return '-' + filename[lastUnderscore + 1:]
    
def isBlackboardGeneratedFile(filename):
    pattern = re.compile('.+\d{4}\-\d{2}\-\d{2}\-\d{2}\-\d{2}\-\d{2}.txt')
    return pattern.match(filename)
    
def changeToWorkingDirectory():
    os.chdir(sys.argv[1]) 
        
if __name__ == '__main__':
    bbcleanup()

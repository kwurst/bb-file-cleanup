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

# Get directory from command line arguments
dir = (sys.argv)[1]

# Change directory
os.chdir(dir)

# Get a list of all files (not directories) (from http://stackoverflow.com/a/3207973)
onlyfiles = [ f for f in os.listdir(dir) if os.path.isfile(os.path.join(os.curdir,f)) ]

# Get rid of spaces in filenames
for f in onlyfiles:
    os.rename(f, f.replace(' ', ''))

# Get the list of all .txt files
txtfiles = [ f for f in os.listdir(dir) if os.path.isfile(os.path.join(os.curdir,f)) and '.txt' in f]

# Get rid of Bb .txt files that have no student text data or comments
#   and rename remaining files to username.txt
for f in txtfiles:
    if '_attempt' in f:
        file = open(f)
        contents = file.read()
        file.close()
        if 'There are no student comments for this assignment' in contents and \
           'There is no student submission text data for this assignment.' in contents:
            os.remove(f)
            print('Deleted', f)
        else:
            first = f.find('_')          # location of first underscore
            second = f.find('_',first+1) # location of second underscore
            newf = f[first+1:second] + '.txt'
            os.rename(f, newf)
            print('Renamed', f, 'to', newf)
            
# Get the list of all non-.txt files
nontxtfiles = [ f for f in os.listdir(dir) if os.path.isfile(os.path.join(os.curdir,f)) and not '.txt' in f]

# Find all the Bb assignment files, which are formatted like:
#     assignmentname_username_attempt_datetime_studentfilename.ext
# Rename the file to username-studentfilename.ext
for f in onlyfiles:
    if '_attempt_' in f:
        first = f.find('_')          # location of first underscore
        second = f.find('_',first+1) # location of second underscore
        last = f.rfind('_')          # location of last underscore
        newf = f[first+1:second] + '-' + f[last+1:]
        os.rename(f, newf)
        print('Renamed', f, 'to', newf)
        

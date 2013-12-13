# Copyright (C) 2013 Karl R. Wurst
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



# Cleans up assignment files downloaded from Blackboard's gradebook
# by deleting all .txt files with no student text data or comments
# and renaming all the remaining files to username.ext

# Call as:
# python BbCleanup.py directory

import sys
from os import chdir, listdir, curdir, remove, rename
from os.path import isfile, join

# Get directory from command line arguments
dir = (sys.argv)[1]

# Change directory
chdir(dir)

# Get a list of all files (not directories)
onlyfiles = [ f for f in listdir(dir) if isfile(join(curdir,f)) ]

# Get the list of all .txt files
txtfiles = [ f for f in onlyfiles if '.txt' in f ]

# Get rid of Bb .txt files that have no student text data or comments
for f in txtfiles:
    file = open(f)
    contents = file.read()
    file.close()
    if 'There are no student comments for this assignment' in contents and \
       'There is no student submission text data for this assignment.' in contents:
        remove(f)
        print('Deleted', f)

# Get the list of remaining files
onlyfiles = [ f for f in listdir(dir) if isfile(join(curdir,f)) ]

# Find all the Bb assignment files, which are formatted like:
#     assignmentname_username_attempt_date_studentfilename.ext
# Rename the file to username.ext
for f in onlyfiles:
    if '_attempt_' in f:
        first = f.find('_') # location of first underscore
        second = f.find('_',first+1) # location of second underscore
        extension = f[f.rfind('.'):] # get file extension
        newf = f[first+1:second] + extension
        rename(f, newf)
        print('Renamed', f, 'to', newf)
        

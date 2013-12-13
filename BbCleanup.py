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

from os import chdir, listdir, curdir
from os.path import isfile, join


# Get command line arguments
args = str(sys.argv)
dir = args[1]

# Change to working directory
chdir(dir)

# Get a list of all files (not directories)
onlyfiles = [ f for f in listdir() if isfile(join(curdir,f)) ]

# Get rid of Bb .txt files that have no student comments

# get list of all .txt files
txtfiles = [ f for f in onlyfiles if '.txt' in f) ]

for f in txtfiles:
    file = open(f)
    contents = file.read()
    file.close()
    if 'There are no student comments for this assignment' in contents and \
       'There is no student submission text data for this assignment.' in contents:
        os.remove(f)


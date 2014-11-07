bb-file-cleanup
===============

Cleans up Blackboard assignment files downloaded *in bulk* from the gradebook

When you download all the files for a specific assignment as a *.zip* file 
from the Blackboard gradebook, two undesirable things happen:

1. The student files are renamed from *filename.ext* to *assignmentname_username*\_attempt\_*datetime_filename.ext*
2. A text file is created for each student named *assignmentname_username*\_attempt\_*datetime*.txt even if the student has not entered any text data or comments.

This script will:

1. Delete all .txt files with no student text data or comments
2. Rename remaining .txt files to *username*.txt
3. Rename all other files to *username*-*userfilename*.*ext*

Call the script as:

> python bbcleanup.py *directory-to-cleanup*


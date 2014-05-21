Bb-file-cleanup
===============

Cleans up Blackboard assignment files downloaded from the gradebook

When you download assignment files from the Blackboard gradebook, two undesirable things happen:

1. The student files are renamed from filename.ext to assignmentname_username_attempt_datetime_filename.ext
2. A text file is created for each student named assignmentname_username_attempt_datetime.txt even if the student has not entered any text data or comments.

This script will:

1. Delete all comment files that contain no text data and no comment.
2. Rename all other files to username-filename.ext

Call the script as:

> python BbCleanup.py *directory-to-cleanup*


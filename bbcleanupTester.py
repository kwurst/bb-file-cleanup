import unittest
from bbcleanup import *


class BbcleanupTester(unittest.TestCase):

    def test_getTextFileListFromFileList_emptyList(self):
        self.assertEqual([], getTextFileListFromFileList([]))
        
    def test_getTextFileListFromFileList_nonEmptyListWithNoTextFiles(self):
        self.assertEqual([], getTextFileListFromFileList(['README.md', 'a.py']))

    def test_getTextFileListFromFileList_nonEmptyListWithTextFiles(self):
        self.assertEqual(['a.txt', 'b.txt'], getTextFileListFromFileList(['README.md', 'a.txt', 'a.py', 'b.txt', 'c.txt.py']))

if __name__ == '__main__':
    unittest.main()

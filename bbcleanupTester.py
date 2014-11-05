import unittest
import os.path
import io

from bbcleanup import *

class BbcleanupTester(unittest.TestCase):
    
    def setUp(self):
        self.system_isfile = os.path.isfile
        os.path.isfile = mock_isfile
        
    def tearDown(self):
        os.path.isfile = self.system_isfile

    def test_isTextFile_notTextFile(self):
        self.assertFalse(isTextFile('a.pdf'))
        
    def test_isTextFile_txtAtEnd(self):
        self.assertTrue(isTextFile('a.txt'))
        
    def test_isTextFile_txtInMiddle(self):
        self.assertFalse(isTextFile('a.txt.pdf'))
   
    def test_filterForFilesOnly_emptyList(self):
        self.assertEqual([], filterForFilesOnly([]))

    def test_filterForFilesOnly_listWithNoFiles(self):
        self.assertEqual([], filterForFilesOnly(['.git', 'src']))

    def test_filterForFilesOnly_listWithFiles(self):
        self.assertEqual(['a.pdf', 'b.txt'], 
                         filterForFilesOnly(['a.pdf', '.git', 'src', 'b.txt']))
        
    def test_removeSpacesAndParentheses_emptyString(self):
        self.assertEqual('', removeSpacesAndParentheses(''))

    def test_removeSpacesAndParentheses_stringWithParentheses(self):
        self.assertEqual('foobarbaz', removeSpacesAndParentheses('foo(bar)baz'))

    def test_removeSpacesAndParentheses_stringWithSpaces(self):
        self.assertEqual('foobar', removeSpacesAndParentheses('foo  bar'))
        
    def test_unmungeBlackboardFileNames_emptyList(self):
        self.assertEqual([], unmungeBlackboardFileNames([]))

    def test_unmungeBlackboardFileNames_emptyList(self):
        self.assertEqual(['jdoe3-chapter13.pdf', 'jdoe3.txt'], 
                         unmungeBlackboardFileNames(['Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38_chapter 13.pdf',
                                                     'Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38.txt']))

def mock_isfile(path):
    directories = ['src', '.git']
    if path in directories:
        return False
    else:
        return True
    
if __name__ == '__main__':
    unittest.main()

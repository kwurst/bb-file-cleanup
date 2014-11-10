import unittest
import os.path

from bbcleanup import *

class BbcleanupTester(unittest.TestCase):
    
    def setUp(self):
        self.system_isfile = os.path.isfile
        os.path.isfile = mock_isfile
        
    def tearDown(self):
        os.path.isfile = self.system_isfile

    def test_isTextFile(self):
        self.assertFalse(isTextFile('a.pdf'))
        self.assertTrue(isTextFile('a.txt'))
        self.assertFalse(isTextFile('a.txt.pdf'))
        
    def test_isAttemptFile(self):
        self.assertFalse(isAttemptFile('a.pdf'))
        self.assertTrue(isAttemptFile('a_attempt_.txt'))
   
    def test_filterForFilesOnly(self):
        self.assertEqual([], filterForFilesOnly([]))
        self.assertEqual([], filterForFilesOnly(['.git', 'src']))
        self.assertEqual(['a.pdf', 'b.txt'], 
                         filterForFilesOnly(['a.pdf', '.git', 'src', 'b.txt']))
        
    def test_removeSpacesAndParentheses(self):
        self.assertEqual('', removeSpacesAndParentheses(''))
        self.assertEqual('foobarbaz', removeSpacesAndParentheses('foo(bar)baz'))
        self.assertEqual('foobar', removeSpacesAndParentheses('foo  bar'))
        
    def test_unmungeBlackboardFileNames(self):
        self.assertEqual([], unmungeBlackboardFilenames([]))
        self.assertEqual(['jdoe3-chapter13.pdf', 'jdoe3.txt'], 
                         unmungeBlackboardFilenames(['Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38_chapter 13.pdf',
                                                     'Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38.txt']))
        
    def test_getUsername(self):
        self.assertEqual('jdoe3', getUsername('Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38_chapter 13.pdf'))
        self.assertEqual('jdoe3', getUsername('Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38.txt'))
        
    def test_getSubmittedFilename(self):
        self.assertEqual('-chapter 13.pdf', getSubmittedFilename('Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38_chapter 13.pdf'))
        self.assertEqual('.txt', getSubmittedFilename('Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38.txt'))
        
def mock_isfile(path):
    directories = ['src', '.git']
    if path in directories:
        return False
    else:
        return True
        
if __name__ == '__main__':
    unittest.main()
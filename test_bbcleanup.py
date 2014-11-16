import unittest
import os.path
import mockfs
from unittest.mock import patch

from bbcleanup import *

class BbcleanupTester(unittest.TestCase):
    
    def setUp(self):
        self.system_isfile = os.path.isfile
        os.path.isfile = mock_isfile
        
    def tearDown(self):
        os.path.isfile = self.system_isfile

    def test_bbcleanup(self):
        fs = mockfs.MockFileSystem()
        fs.setDictionary({
            'Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38_chapter (13).pdf':'',
            'Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38.txt': '''
                There are no student comments for this assignment
                There is no student submission text data for this assignment.
                ''',
        })

        with patch.multiple(os,
                listdir=fs.listdir,
                rename=fs.rename,
                chdir=fs.chdir,
                remove=fs.remove):
            with patch('os.path.isfile', fs.isfile):
                with patch('bbcleanup.getFileContents', fs.getFileContents):
                    with patch('sys.argv', ['', 'anything']):
                        bbcleanup()

        self.assertListEqual(['jdoe3-chapter13.pdf'], fs.listdir())

    def test_isAttemptFile(self):
        self.assertFalse(isAttemptFile('a.pdf'))
        self.assertTrue(isAttemptFile('a_attempt_.txt'))
   
    def test_filterForAttemptFiles(self):
        self.assertEqual([], filterForAttemptFiles([]))
        self.assertEqual([], filterForAttemptFiles(['.git', 'src']))
        self.assertEqual(['a_attempt_b.pdf', 'b_attempt_c.txt'], 
                         filterForAttemptFiles(['a_attempt_b.pdf', '.git', 'src', 'b_attempt_c.txt', 'c.txt']))
        
    def test_removeSpacesAndParentheses(self):
        self.assertEqual('', removeSpacesAndParentheses(''))
        self.assertEqual('foobarbaz', removeSpacesAndParentheses('foo(bar)baz'))
        self.assertEqual('foobar', removeSpacesAndParentheses('foo  bar'))
        
    def test_fixBlackboardFileName(self):
        self.assertEqual('jdoe3-chapter13.pdf',
                         fixBlackboardFilename('Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38_chapter 13.pdf'))
        self.assertEqual('jdoe3.txt',
                         fixBlackboardFilename('Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38.txt'))
        
    def test_getUsername(self):
        self.assertEqual('jdoe3', getUsername('Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38_chapter 13.pdf'))
        self.assertEqual('jdoe3', getUsername('Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38.txt'))
        
    def test_getSubmittedFilename(self):
        self.assertEqual('-chapter 13.pdf', getSubmittedFilename('Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38_chapter 13.pdf'))
        self.assertEqual('.txt', getSubmittedFilename('Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38.txt'))
        self.assertEqual('-chapter 13.txt', getSubmittedFilename('Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38_chapter 13.txt'))
        
    def test_isBbCommentFile(self):
        self.assertTrue(isBlackboardGeneratedFile('Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38.txt'))
        self.assertFalse(isBlackboardGeneratedFile('Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38_chapter 13.pdf'))
        self.assertFalse(isBlackboardGeneratedFile('Chapter 13 Problems_jdoe3_attempt_2014-04-30-21-02-38_chapter 13.txt'))

def mock_isfile(path):
    directories = ['src', '.git']
    if path in directories:
        return False
    else:
        return True
        
if __name__ == '__main__':
    unittest.main()

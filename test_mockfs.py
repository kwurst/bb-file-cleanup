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

import unittest
import mockfs

class MockfsTests(unittest.TestCase):
    
    def setUp(self):
        self.fs = mockfs.MockFileSystem()
        
    def tearDown(self):
        pass

    def test_getDictionary(self):
        d = {'one': 'contents'}
        self.fs.setDictionary(d)
        dd = self.fs.getDictionary()
        self.assertDictEqual(d, dd)

    def test_listdir(self):
        self.fs.setDictionary({'two':'', 'one':''})
        listing = self.fs.listdir()
        self.assertListEqual(sorted(['two','one']), listing)

    def test_getFileContents(self):
        self.fs.setDictionary({'two':'contents'})
        contents = self.fs.getFileContents('two')
        self.assertEqual('contents', contents)

    def test_isfile(self):
        self.fs.setDictionary({'afile':'', 'adir':{}})
        afile = self.fs.isfile('afile')
        adir = self.fs.isfile('adir')
        self.assertTrue(afile)
        self.assertFalse(adir)

    def test_remove(self):
        self.fs.setDictionary({'afile':''})
        self.fs.remove('afile')
        self.assertNotIn('afile', self.fs.listdir())

    def test_rename(self):
        self.fs.setDictionary({'afile':''})
        self.fs.rename('afile', 'bfile')
        self.assertListEqual(['bfile'], self.fs.listdir())

    def test_chdir(self):
        self.fs.setDictionary({'afile':''})
        self.fs.chdir('blah/blah/blee/blee')
        self.assertDictEqual({'afile':''}, self.fs.getDictionary())

if __name__ == '__main__':
    unittest.main()

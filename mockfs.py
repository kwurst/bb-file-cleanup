class MockFileSystem:
    def __init__(self):
        self.dictionary = {}

    def setDictionary(self, dictionary):
        self.dictionary = dictionary

    def getDictionary(self):
        return self.dictionary

    def chdir(self, path):
        pass

    def listdir(self):
        return sorted(self.dictionary.keys())

    def getFileContents(self, filename):
        return self.dictionary[filename]

    def isfile(self, filename):
        return isinstance(self.dictionary[filename], str)

    def remove(self, filename):
        del self.dictionary[filename]

    def rename(self, currentFilename, newFilename):
        self.dictionary[newFilename] = self.dictionary[currentFilename]
        self.remove(currentFilename)


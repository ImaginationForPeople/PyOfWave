import unittest
import tempfile, os

from pyofwave.storage.backends.files import FileStore

class TestFileStore(unittest.TestCase):
    def setUp(self):
        self.storage = FileStore(path=os.path.join(tempfile.gettempdir(), 'pyofwave-fs-test/'),
                                 checkDomain=True)

    def testNewDocument(self):
        self.storage.newDocument('pyofwave.info!y7_8t4#')

    def testCreateGetDocument(self):
        doc_uri = 'pyofwave.info!Zz42b3'
        self.storage.newDocument(doc_uri)
        doc_content = self.storage.getDocument(doc_uri)

        assert(doc_content == '')

    def testGetDocumentVersion(self):
        assert(False)

    def testFilename(self):
        assert(False)
    
    def testApplyDelta(self):
        assert(False)




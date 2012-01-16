import unittest
import tempfile
import os

from pyofwave.core.datasource import DataStoreError
from pyofwave.core.document.blip import Blip
from pyofwave.storage.backends.files import FileStore


class TestFileStore(unittest.TestCase):
    def setUp(self):
        self.temp_dir = os.path.join(tempfile.gettempdir(), 'pyofwave-fs-test/')
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        
        for filename in os.listdir(self.temp_dir):
            filepath = os.path.join(self.temp_dir, filename)
            os.remove(filepath)

        self.storage = FileStore(path=self.temp_dir,
                                 checkDomain=True)

    def testSaveBlip(self):
        content = """<doc>
                        <select href="foo" range="2" version="2" />
                        <text>hello world</text>
                    </doc>"""

        document = Blip(uri="pyofwave.info!foo", content=content)

        self.storage.save_document(aDocument=document)
        expected_file = os.path.join(self.temp_dir, "foo")
        self.assertTrue(os.path.exists(expected_file))

        content = """<doc>
                        <text>hello world</text>
                    </doc>"""

        document = Blip(uri="pyofwave.info!bar", content=content)
        self.assertRaises(DataStoreError, self.storage.save_document, (document))
        not_expected_file = os.path.join(self.temp_dir, "bar")
        self.assertFalse(os.path.exists(not_expected_file))

    def testGetDocument(self):
        uri = "pyofwave.info!foo"

        content = """<doc>
                        <select href="foo" range="2" version="2" />
                        <text>hello world</text>
                    </doc>"""
        document = Blip(uri=uri, content=content)

        self.storage.save_document(aDocument=document)

        retrieved_document = self.storage.get_document(doc_uri=uri)
        self.assertTrue(retrieved_document != None)

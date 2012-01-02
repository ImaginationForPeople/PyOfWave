import unittest

from pyofwave.core.document import DocumentItems

class TestDocumentItems(unittest.TestCase):
    def setUp(self):
        self.items = DocumentItems()

    def testInsertions(self):
        self.items.insert_start_tag(0, "p")
        
        self.items.insert_character(1, u'h')
        self.items.insert_characters(2, u'ello')

        self.items.insert_end_tag(7, "p")

        assert(self.items, '<p>hello</p>')



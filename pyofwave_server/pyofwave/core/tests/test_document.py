import unittest

from pyofwave.core.document.annotation import Annotation, Annotations
from pyofwave.core.document.item import DocumentItemStream

class TestDocumentItemStream(unittest.TestCase):
    def setUp(self):
        self.items = DocumentItemStream()

    def testInsertions(self):
        self.assertRaises(IndexError,
                          self.items.insert_characters,
                          position=2,
                          characters=u'hello')
        self.assertEquals(str(self.items), "")        

        self.items.insert_start_tag(0, "p")
        self.assertEquals(str(self.items), "<p>")
        
        self.items.insert_character(1, u'h')
        self.assertEquals(str(self.items), "<p>h")
                
        self.items.insert_characters(2, u'ello')
        self.assertEquals(str(self.items), "<p>hello")        

        self.items.insert_end_tag(6, "p")
        self.assertEquals(str(self.items), '<p>hello</p>')


    def testDeletions(self):
        self.items.insert_start_tag(0, "plop")
        self.assertEquals(str(self.items), "<plop>")        

        self.items.insert_characters(1, "hey")
        self.assertEquals(str(self.items), "<plop>hey")

        self.items.insert_end_tag(4, "plop")
        self.assertEquals(str(self.items), "<plop>hey</plop>")
        
        self.items.remove_item_at(1)
        self.items.remove_item_at(1)
        self.items.remove_item_at(1)
        self.assertEquals(str(self.items), "<plop></plop>")

        self.items.remove_item_at(0)
        self.assertEquals(str(self.items), "</plop>")


class TestAnnotation(unittest.TestCase):
    def setUp(self):
        self.ann = Annotation(name='color', value='red',
                              start_position=5,
                              end_position=10)

    def testShift(self):
        assert(self.ann.start_position == 5)
        assert(self.ann.end_position == 10)

        # shift before annotation
        self.ann.shift(3, 3)

        assert(self.ann.start_position == 8)
        assert(self.ann.end_position == 13)

        # shift after annotation
        self.ann.shift(25, 5)

        assert(self.ann.start_position == 8)
        assert(self.ann.end_position == 13)

        # shift inside annotation
        self.ann.shift(10, 1)

        assert(self.ann.start_position == 8)
        assert(self.ann.end_position == 14)

class TestAnnotations(unittest.TestCase):
    def setUp(self):
        self.anns = Annotations()

    def testAdd(self):
        self.anns.add(name='color',
                      value='red',
                      start_position=2,
                      end_position=10)

        self.assertEquals(len(self.anns), 1)

        col_ann = Annotation(name='color',
                             value='red',
                             start_position=2,
                             end_position=10)
        assert(col_ann in self.anns)

        # Add another annotation, distinct name, overlapping position
        self.anns.add(name='weight',
                      value='bold',
                      start_position=0,
                      end_position=8)
        self.assertEquals(len(self.anns), 2)

        weight_ann = Annotation(name='weight',
                                value='bold',
                                start_position=0,
                                end_position=8)

        assert(weight_ann in self.anns)
        self.assertEquals(len(self.anns['weight']), 1)

        # same name and value, different position
        self.anns.add(name='weight',
                      value='bold',
                      start_position=10,
                      end_position=12)

        self.assertEquals(len(self.anns), 2)
        self.assertEquals(len(self.anns['weight']), 2)

        # same name and value, overlapping
        self.anns.add(name='weight',
                      value='bold',
                      start_position=8,
                      end_position=9)
        self.assertEquals(len(self.anns), 2)
        self.assertEquals(len(self.anns['weight']), 2)

        assert(weight_ann not in self.anns)

        # same name and value, should connect both 'weight' annotations
        self.anns.add(name='weight',
                      value='bold',
                      start_position=9,
                      end_position=13)
        self.assertEquals(len(self.anns), 2)
        self.assertEquals(len(self.anns['weight']), 1)
        
        



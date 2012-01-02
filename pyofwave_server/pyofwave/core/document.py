from collections import defaultdict

import pyofwave.storage

class Annotation(object):
    """
    An annotation is an immutable key-value pair of metadata over a
    range of DocumentItems.
    
    Example uses of annotations include styling text, supplying
    spelling corrections, and links to refer that area of text to
    another document or web site.
    """
    def __init__(self, name, value, start_position, end_position):
        self.name = name
        self.value = value
        self.start_position = start_position
        self.end_position = end_position

    def shift(self, position, amount):
        """
        Shifts this annotation by amount if it is on a range that is
        after or covers the given position.
        """
        if self.start_position >= position:
            self.start_position += amount
            
        if self.end_position >= position:
            self.end_position += amount

    def __hash__(self):
        # XXX: This hash function is wrong, collisions are too easy!
        return hash(self.name) | hash(self.value) | hash(self.start_position) | hash(self.end_position)

    def __unicode__(self):
        return u"{'%s': '%s'}@[%d-%d]" % (self.name,
                                          self.value,
                                          self.start_position,
                                          self.end_position)


class Annotations(object):
    """
    A set of Annotations for a document.
    Handles overlapping.
    """
    def __init__(self):
        self._store = defaultdict(list())

    def add(self, name, value, start_position, end_position):
        new_list = list()
        for annotation in self._store[name]:
            # Non-overlapping annotation
            if (start_position > annotation.end_position) or \
                    (end_position < annotation.start_position):
                new_list.append(annotation)

            # Overlapping: need to merge
            elif annotation.value == value:
                start_position = min(annotation.start_position, start_position)
                end_position = max(annotation.end_position, end_position)

            # Overlapping: different values. Make room for ours
            else:
                # Cut the tail of the old annotation if required
                if annotation.start_position < start_position:
                    new_list.append(Annotation(annotation.name, annotation.value,
                                               annotation.start_position,
                                               start_position)
                                    )
                # Cut the head of the old annotation if required
                if annotation.end_position > end_position:
                    new_list.append(Annotation(annotation.name, annotation.value,
                                               end_position,
                                               annotation.end_position)
                                    )

        new_list.append(Annotation(name, value, start_position, end_position))
        
        self._store[name] = new_list
    
class DocumentItems(list):
    """
    From: http://www.waveprotocol.org/whitepapers/operational-transform

    In Google Wave, every character, start tag or end tag in a
    document is called an item. Gaps between items are called
    positions. Position 0 is before the first item.

    [<p>] [h] [e] [l] [l] [o] [</p>]
    0....1...2...3...4...5...6......7
    """
    def insert_start_tag(self, position, start_tag):
        """
        Insert a start tag, such as "<p>". start_tag should be "p" for
        example.
        Return the cursor position
        """
        # XXX: Use lxml
        self.insert(position, "<%s>" % start_tag)
        return position + 1

    def insert_end_tag(self, position, end_tag):
        """
        Insert an ending tag, such as "</p>". end_tag should be "p"
        for example.
        Return the cursor position
        """
        # XXX: Use lxml
        self.insert(position, "</%s>" % end_tag)
        return position + 1

    def insert_character(self, position, character):
        """
        Insert a single character, return the cursor position.
        Return the cursor position.
        """
        self.insert(position, character)
        return position + 1

    def insert_characters(self, position, characters):
        """
        Insert a string at the given position.
        Return the cursor position
        """
        for character in characters:
            self.insert_character(position, character)

    def remove_item_at(self, position):
        """
        Remove the item at the given position.
        Return the removed item
        """
        return self.pop(position)

    def __str__(self):
        return "".join(self)
    

class Document(object):
    """
    A document is piece of XML linked to an URI, that can be stored
    into a datastore and on which operations can be applied to
    transform it.
    """
    def __init__(self, uri, content="", aDataStore=None):
        self.uri = uri
        self.content = content
        self.datastore = aDataStore

    @classmethod
    def load(klass, uri, aDataStore=None):
        """
        Loads a document from a given datastore, or from the
        configured default one.
        """
        if not aDataStore:
            aDataStore = pyofwave.storage.datastore

        return aDataStore.get_document(uri)
        

    def save(self, aDataStore=None):
        """
        Persist a Document into the given DataStore, or the one where
        the document comes from.
        """
        if not aDataStore:
            if self.datastore:
                aDataStore = self.datastore
            else:
                # XXX: Use a real exception
                raise "This document is not linked to a datastore or none was specified"
            
        return aDataStore.save_document(self)
                
    @property
    def length(self):
        """
        The length of the xml content
        """
        return len(self.content)

    def __str__(self):
        return "%s: %s" % (self.uri, self.content)






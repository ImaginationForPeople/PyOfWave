import pyofwave.storage

class Document(object):
    """
    Abstract Class.
    
    A document is a unit of content attached to a wavelet. Two basic
    types of documents exist within the Wave API: Blips and Data
    Documents.

    Although blips and data documents are each "documents", in
    practice, you treat them quite separately. Each blip consists of
    markup (similar to XML) which can be retrieved, modified or added by
    the API. Generally, you manage the blip through convenience methods
    rather than through direct manipulation of the XML data
    structure. Blips are very structured, while data documents may have no
    intrinsic schema (though often contain their one self-defined
    structure).
    
    A Document is referenced by its URI, can be stored into a datastore and
    operations can be applied to transform it.
    """
    def __init__(self, uri, aDataStore=None):
        self.uri = uri
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
                

    def __str__(self):
        return "%s: %s" % (self.uri, self.content)

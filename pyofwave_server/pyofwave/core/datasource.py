"""
Contains standard interfaces for dataSources. 
"""
from zope import interface

class DataSource(interface.Interface):
    """
    Standard interface for a dataSource. 
    """
    def save_document(aDocument):
        """
        generate a new document.
        """
        raise NotImplementedError

    def get_document(doc_uri):
        """
        returns the specified document.
        """
        raise NotImplementedError

    def get_document_version(doc_uri, version):
        """
        Returns the delta for the specified versions. 
        """
        raise NotImplementedError

class DataStoreError(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)


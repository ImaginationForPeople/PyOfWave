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
        Save (or create if not existing) a document
        """
        raise NotImplementedError

    def get_document(doc_uri):
        """
        Retrieve the document from the DataSource.
        """
        raise NotImplementedError

    def get_document_version(doc_uri, version):
        """
        Retrieve the document at the specified version. 
        """
        raise NotImplementedError


class DataStoreError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

"""
Provides a storage class which uses .wave & .ver files to save data.
Not recommended for production use.  
"""
import os

from lxml import etree
from zope.interface import implements

from pyofwave.conf import settings
from pyofwave.core.datasource import DataSource, DataStoreError
from pyofwave.core.document import Document

class FileStore(object):
    """
    A simple data store using files to store waves
    """
    implements(DataSource)    

    def __init__(self, path=None, checkDomain=None):
        self.path = path or settings.FILESTORAGE_PATH
        self.checkDomain = checkDomain or settings.FILESTORAGE_CHECKDOMAIN
        self.dtd = etree.DTD(open("../../docs/protocols/wave protocol DTDs/doc.dtd",  'rb'))

        # Create target dir if necessary
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        
    def save_document(self, aDocument):
        document_path = self._filepath(aDocument.uri)
        try:
            xml_content = etree.fromstring(aDocument.content)
            if self.dtd.validate(xml_content):
                # an existing document with the same name will be erased
                with open(document_path, 'w') as document_file:
                    document_file.write(etree.tostring(xml_content, 
                                                       xml_declaration=True,
                                                       encoding='utf-8',
                                                       pretty_print=True))
            else:
                raise DataStoreError("ERROR: Document can not be saved : xml content is not valid")
        except:
            raise
            

    def get_document(self, doc_uri):
        document_path = self._filepath(doc_uri)
        
        if not os.path.exists(document_path):
            # XXX : should raise an exception ?
            return None
        
        try:
            xml_tree = etree.parse(document_path)
            if self.dtd.validate(xml_tree):
                return Document(uri=doc_uri,
                                content=etree.tostring(xml_tree),
                                aDataStore=self)
            else:
                raise DataStoreError("ERROR: Document can not be saved : xml content is not valid")
        except:
            raise
        

    def get_document_version(self, doc_uri, version):
        raise NotImplementedError

    def _filename(self, doc_uri):
        """
        Given a document URI, return a filename
        """
        if "!" in doc_uri:
            return doc_uri.split("!")[1]
        
        return doc_uri

    def _filepath(self, doc_uri):
        """
        Given a document, return the complete file path
        """
        filename = self._filename(doc_uri)
        filepath = os.path.join(self.path, '%s' % filename)

        return filepath

DataStore = FileStore

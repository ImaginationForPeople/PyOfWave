Data Storage Extensions
***********************

If the existing data storage options don't suit you, you can easily add your own.

1. Preparing the Datasource
===========================

The datasource needs to be set up to be able to store PyOfWave documents before you integrate it. To do this, setup your datasource to store XML and access elements by their ID (which would be in the form of a Wave URL).

2. Implement the Adaptor
========================

Add a new Python file in datasource (doesn't really matter if you put it there) and code::

       from pyofwave.core import datasource
       from zope.interface import implements

       class MyDataStorage(object):
            implements(datasource.Datasource)
    
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

Implement the methods. 

Make sure you allow your users to override the default config by using
variables coming from their :file:`settings.py`. Here's an example::

      from pyofwave.conf import settings

      class MyDataSource(object):
         def __init__(self, path=None, checkDomain=None):
            self.path = path or settings.MYDATASOURCE_PATH
            self.checkDomain = checkDomain or settings.MYDATASOURCE_CHECKDOMAIN


3. Integrate the Adaptor
========================

In your :file:`settings.py` set :py:data:`DATASOURCE_STORAGE` to the
path of your adaptor. For example, to use the file storage backend::

     DATASOURCE_STORAGE = 'storage.files.FileStorage'

Then, declare the variables required by the backend such as::

     FILESTORAGE_PATH = 'waves/'

Also ensure that the applyDelta method is set to observe betaDeltaObservable, ``betaDeltaObservable.addObserver(STORAGE_OBJECT.applyDelta)``.

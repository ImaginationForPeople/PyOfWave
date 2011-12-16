"""
Provides a storage class which uses .wave & .ver files to save data.
Not recommended for production use.  
"""
import os
try:
   import cPickle as pickle
except:
   import pickle

from zope.interface import implements

from pyofwave.conf import settings
from pyofwave.core import delta
from pyofwave.core.datasource import DataSource

class FileStore(object):
   """
   A simple data store using files to store waves
   """
   implements(DataSource)   

   def __init__(self, path=None, checkDomain=None):
      self.path = path or settings.FILESTORAGE_PATH
      self.checkDomain = checkDomain or settings.FILESTORAGE_CHECKDOMAIN

      # Create target dir if necessary
      if not os.path.exists(self.path):
         os.makedirs(self.path)
      
   def applyDelta(self, doc, delta):
      doc = self._filename(doc)
      if not doc: 
         return
      
      # update .wave file
      wavelet = delta.update(self.getDocument(doc)) # apply the delta
      f = open("%s.wave" % doc, 'w') # overwrite
      pickle.dump(wavelet, f)
      f.close()
      
      # append onto .ver file
      f = open(doc + ".ver", 'a') # append at end of file.
      pickle.dump(delta, f)
      f.close()

   def newDocument(self, doc):
      doc = self._filename(doc, "newDocument", doc)

      if not isinstance(doc, str):
         # XXX: Shouldn't we raise an exception here?
         return

      filepath = self._filepath(doc)

      # empty ".wave" file
      wave_filepath = filepath + '.wave'
      fd = open(wave_filepath, 'w')
      data = pickle.dumps("")
      fd.write(data)
      fd.close()

      # empty ".ver" file
      ver_filepath = filepath + '.ver'
      fd = open(ver_filepath, 'w')
      data = pickle.dumps("")
      fd.write(data)
      fd.close()

   def getDocument(self, doc_uri):
      if not isinstance(doc_uri, str):
         # XXX: Shouldn't we raise an exception here?
         return doc

      filepath = self._filepath(doc_uri, "getDocument", doc_uri)

      # unpickle current 
      wave_filepath = '%s.wave' % filepath
      fd = open(wave_filepath, 'rb')
      doc = pickle.load(fd)

      return doc

   def getDocumentVersion(self, doc, start, end, limit):
      doc = self._filename(doc, "getDocumentVersion", doc, start, end, limit)

      if not isinstance(doc, str):
         # XXX: Shouldn't we raise an exception here?
         return doc

      if (end - start) > limit: 
         end = start + limit # ensure the limit is met.

      # load data
      f = open(doc+".ver", 'r')
      res = []
      i = 0
      
      while delta or i >= end:
         delta = pickle.load(f)
         res.append(delta)

      return res[start:end]

   def _filename(self, doc, call=None, *args):
      """
      Given a document URI, return a filename
      """
      if "!" in doc:
         doc = doc.split("!")

         # if not in this domain, call the sucessor.
         if doc[0] != settings.DOMAIN and not self.checkDomain: 
            if call: 
               return getattr(self.successor, call)(*args)
            return None
         
         return self.path + doc[1]
      
      return doc

   def _filepath(self, doc, call=None, *args):
      """
      Given a document, return the complete file path
      """
      filename = self._filename(doc, call, *args)
      filepath = os.path.join(self.path, '%s' % filename)

      return filepath

DataStore = FileStore

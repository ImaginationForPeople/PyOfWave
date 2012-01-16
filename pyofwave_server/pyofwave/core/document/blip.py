from . import Document

from .annotation import Annotations
from .item import DocumentItemStream

class Blip(Document):
    """
    A Blip is the basic unit of conversation and consists of a single
    message which appears on a wavelet. Blips may also contain other
    blips as children, forming a blip hierarchy. Each wavelet always
    consists of at least one root blip.
    """
    def __init__(self, uri, content="", aDataStore=None):
        Document.__init__(self, uri, aDataStore)
        self.content = content

        self.annotations = Annotations()
        self.stream = DocumentItemStream()
        
    
    def __len__(self):
        """
        The length of the xml content
        """
        return len(self.content)








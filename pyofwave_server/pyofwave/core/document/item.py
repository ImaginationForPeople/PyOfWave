class DocumentItemStream(object):
    """
    From: http://www.waveprotocol.org/whitepapers/operational-transform

    In Google Wave, every character, start tag or end tag in a
    document is called an item. Gaps between items are called
    positions. Position 0 is before the first item.

    [<p>] [h] [e] [l] [l] [o] [</p>]
    0....1...2...3...4...5...6......7
    """
    def __init__(self):
        self._items = list()

    def _checkCursor(self, position):
        """
        Check if the position is in the correct range
        XXX: Maybe move to list implementation?
        """
        if not (0 <= position <= len(self._items)):
            raise IndexError
                    
    def insert_start_tag(self, position, start_tag):
        """
        Insert a start tag, such as "<p>". start_tag should be "p" for
        example.
        Return the cursor position
        """
        self._checkCursor(position)
        # XXX: Use lxml
        self._items.insert(position, "<%s>" % start_tag)
        return position + 1

    def insert_end_tag(self, position, end_tag):
        """
        Insert an ending tag, such as "</p>". end_tag should be "p"
        for example.
        Return the cursor position
        """
        self._checkCursor(position)
        # XXX: Use lxml
        self._items.insert(position, "</%s>" % end_tag)
        return position + 1

    def insert_character(self, position, character):
        """
        Insert a single character, return the cursor position.
        Return the cursor position.
        """
        self._checkCursor(position)
        
        self._items.insert(position, character)
        return position + 1

    def insert_characters(self, position, characters):
        """
        Insert a string at the given position.
        Return the cursor position
        """
        self._checkCursor(position)
        
        for character in reversed(characters):
            self.insert_character(position, character)

    def remove_item_at(self, position):
        """
        Remove the item at the given position.
        Return the removed item
        """
        self._checkCursor(position)            
        return self._items.pop(position)

    def __str__(self):
        return u"".join(self._items)
    






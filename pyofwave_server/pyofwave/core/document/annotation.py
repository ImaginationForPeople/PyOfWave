from collections import defaultdict

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

        # XXX: remove this?
        assert(start_position < end_position)
        
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

    def __unicode__(self):
        return u"{'%s': '%s'}@[%d-%d]" % (self.name,
                                          self.value,
                                          self.start_position,
                                          self.end_position)

    def __eq__(self, otherAnnotation):
        return (self.name == otherAnnotation.name and \
                    self.value == otherAnnotation.value and \
                    self.start_position == otherAnnotation.start_position and \
                    self.end_position == otherAnnotation.end_position)
    

class Annotations(object):
    """
    A set of Annotations for a document.
    Handles overlapping and merge if necessary.
    """
    def __init__(self):
        self._store = defaultdict(list)

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


    def __contains__(self, anAnnotation):
        if anAnnotation.name in self._store:
            return anAnnotation in self._store[anAnnotation.name]

        return False

    def __iter__(self):
        return self._store.__iter__()

    def __getitem__(self, key):
        return self._store[key]

    def __len__(self):
        return self._store.__len__()

    def __str__(self):
        return str(self._store)


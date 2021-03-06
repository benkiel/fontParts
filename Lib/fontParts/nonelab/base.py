class RBaseObject(object):

    wrapClass = None

    def _init(self, wrap=None):
        if wrap is None and self.wrapClass is not None:
            wrap = self.wrapClass()
        if wrap is not None:
            self._wrapped = wrap

    def __eq__(self, other):
        if hasattr(other, "_wrapped"):
            return self._wrapped == other._wrapped
        return False

    def naked(self):
        if hasattr(self, "_wrapped"):
            return self._wrapped
        return None

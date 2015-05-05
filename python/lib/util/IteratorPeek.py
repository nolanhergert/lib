"""
A class that allows you to peek into the future of the iterator
"""

class IteratorPeek:
    def __init__(self, iter):
        self.iter = iter
        self.buffer = []

    def __iter__(self):
        return self

    def next(self):
        if self.buffer:
            return self.buffer.pop(0)
        else:
            return self.iter.next()

    def Peek(self, n=None):
        """Return an item n entries ahead in the iteration. If n=None, then
        return the next element """
        if (n == None):
            try:
                nextVal = self.iter.next()
                self.buffer.append(nextVal)
                return nextVal
            except StopIteration:
                return None
        else:
            while n >= len(self.buffer):
                try:
                    self.buffer.append(self.iter.next())
                except StopIteration:
                    return None
            return self.buffer[n]
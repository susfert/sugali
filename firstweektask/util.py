from collections import Counter
from itertools import chain
from string import punctuation

try:
  from nltk.tokenize import word_tokenize
except ImportError:
  def word_tokenize(text):
    """ Stripped down version of NTLK's word_tokenize. """ 
    for ch in text:
      if ch in punctuation:
        text = text.replace(ch, " "+ch+" ")
    return text.split()

try:
  from nltk.probability import FreqDist
  pass
except:
  class FreqDist(Counter):
    """ Strip down version of NLTK's FreqDist. """
    def __init__(self, corpus=None):
      if corpus != None:
        if all(isinstance(i, list) for i in corpus):
          # Flatten lists of lists into a single list.
          _corpus = list(chain(*corpus))
        else:
          _corpus = corpus
        self.update(_corpus)
      
      def __iter__(self):
        """ Iterator function: Returns keys of dict. """
        return iter(self.keys())
      
      def __str__(self):
        """ Descriptor function. """
        items = ['%r: %r' % (s, self[s]) for s in self] 
        return '<FreqDist: %s>' % ', '.join(items)
    
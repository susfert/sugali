# -*- coding: utf-8 -*-

import sys; sys.path.append('../') # Access modules from parent dir.

import tarfile, codecs, os, re
from collections import defaultdict
import cPickle as pickle
from utils import remove_tags

try:
  from bs4 import BeautifulSoup as bs
except:
  from BeautifulSoup import BeautifulSoup as bs
#bs.find_all = getattr(bs, 'find_all',False) or getattr(bs, 'findAll')

ODIN = '../data/odin/odin-full.tar'
ODIN_DIR = '../data/odin/'

def get_odin_examples():
  """
  Extracts the examples from the ODIN igts and returns a defaultdict(list),
  where the keys are the lang iso codes and values are the examples.
  """
  tar = tarfile.open(ODIN)
  docs = defaultdict(list)
  for infile in tar:
    if '.xml' in infile.name: # there's a rogue file in the tar that is not xml.
      lang = infile.name[:-4].lower()
      # Find the <igt>...</igt> in the xml.
      igts = bs(tar.extractfile(infile).read()).findAll('igt')
      for igt in igts:
        # Find the <example>...</example> in the igt.
        examples = bs(unicode(igt)).findAll('example')
        for eg in examples:
          try:
            # Only use triplets lines and assumes that
            # line1: src, line2:eng, line3:gloss
            src, eng, gloss = bs(unicode(eg)).findAll('line')
            src, eng, gloss = map(unicode, [src, eng, gloss])
            docs[lang].append((src, eng, gloss))
            print src, eng, gloss
          except:
            raise; print eg
  return docs

def load_odin_examples():
  """
  Loads odin-docs.pk and return it as a defaultdict(list).
  
  >>> for lang, examples in load_odin_examples():
  >>>   print lang, examples
  """
  # If odin-docs.pk is not available create it.
  if not os.path.exists(ODIN_DIR+'odin-docs.pk'):
    odindocs = get_odin_examples()
    # Outputs the odin igts examples into '../data/odin/odin-docs.pk'.
    with codecs.open(ODIN_DIR+'odin-docs.pk','wb') as fout:
      pickle.dump(odindocs, fout)
  # Loads the pickled file.
  with codecs.open(ODIN_DIR+'odin-docs.pk','rb') as fin2: 
    docs = pickle.load(fin2)
    for lang in docs:
      # the data might be too much for the RAM, so yield instead of return.
      yield (lang, docs[lang])
      
def odin_src_only(outputfile=True, testing=False):
  """ Extracts only the source language tokens from the ODIN IGTs."""
  odinsrc = defaultdict(list)
  for language, documents in sorted(load_odin_examples()):
    for d in documents:
      src = remove_tags(d[0])
      # Removes heading bullets, e.g. (1)... | 1) | ( 12 ) | i. ... | A2. ...
      src = re.sub(r'^\(?\s?\w{1,5}\s*[):.]\s*', '', src)
      src = re.sub(r'^\(?\w{1,5}\s*[):.]\s*', '', src)
      # Joins the morphemes up into words.
      src = re.sub( ' *- *', '', src)
      odinsrc[language].append(src)
    if testing:
      return odinsrc
      
  if outputfile == True:
    with codecs.open(ODIN_DIR+'odin-src.pk','wb') as fout:
      pickle.dump(odinsrc, fout)

def load_odin_src():
  """
  Loads odin-docs.pk and returns it as a defaultdict
  
  >>> for lang, text in load_odin_src():
  >>>   print lang, text
  """
  pass
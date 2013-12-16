# -*- coding: utf-8 -*-

import tarfile, tempfile, os, codecs
from itertools import chain

def word2ngrams(text, n=3, with_word_boundary=False):
  """ Convert text into character ngrams. """
  text = text.lower()
  char_ngrams =  ["".join(j) for j in zip(*[text[i:] for i in range(n)])]
  if with_word_boundary:
    char_ngrams+=["<"+text[:2],text[-2:]+">"]
  return char_ngrams

def sentence2ngrams(text,n=3,with_word_boundary=False):
  """ Takes a document, convert into ngrams"""
  return list(chain(*[word2ngrams(i) for i in text.split()]))

def read_tarfile(intarfile):
  """ Extracts a tarfile to a temp directory, then yield one file at a time. """
  TEMP_DIR = tempfile.mkdtemp()
  with tarfile.open(intarfile) as tf:
    for member in tf.getmembers():
      tf.extract(member, TEMP_DIR)
  
  for infile in os.listdir(TEMP_DIR):
    yield TEMP_DIR+'/'+infile
    
def extract_odin_sentences(intarfile):
  """ Extracts char ngrams features from odin. """
  for infile in read_tarfile(intarfile):
    language = infile.split('/')[-1].split('-')[1].split('.')[0]
    with codecs.open(infile,'r','utf8') as fin:
      for line in fin.readlines():
        sentence, sentence_morphemes, _ , _ ,_ = line.split('\t')
        yield language, sentence

# TODO: requires langtoiso function.
def extract_omniglot_phrases(intarfile):
  """ Extracts char ngrams features from omniglot. """
  for infile in read_tarfile(intarfile):
    language = infile.split('/')[-1].split('-')[1].split('.')[0]
    print language

def extract_udhr_sentences(intarfile):
  """ Extracts char ngrams features from udhr. """
  for infile in read_tarfile(intarfile):
    language = infile.split('/')[-1][:3]
    with codecs.open(infile,'r','utf8') as fin:
      for sentence in fin.readlines():
        yield language, sentence

extract_omniglot_phrases('../../data/omniglot/omniglotphrases.tar')


'''
# Informal tests.
for lang, sent in extract_odin_sentences('../../data/odin/odin-cleaner.tar'):
  print lang, sentence2ngrams(sent)
    
for lang, sent in extract_udhr_sentences('../../data/udhr/udhr-unicode.tar'):
  print lang, sentence2ngrams(sent)
'''  
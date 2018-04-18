# -*- coding: UTF-8 -*-

import re
import nltk  
import nltk.data  
from nltk.tokenize import RegexpTokenizer   
from nltk.stem import WordNetLemmatizer

stop_word = ["i",
            "me",
            "my",
            "myself",
            "we",
            "us",
            "our",
            "ours",
            "ourselves",
            "you",
            "your",
            "yours",
            "yourself",
            "yourselves",
            "he",
            "him",
            "his",
            "himself",
            "she",
            "her",
            "hers",
            "herself",
            "it",
            "its",
            "itself",
            "they",
            "them",
            "their",
            "theirs",
            "themselves",
            "what",
            "which",
            "who",
            "whom",
            "this",
            "that",
            "these",
            "those",
            "am",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "having",
            "do",
            "does",
            "did",
            "doing",
            "will",
            "would",
            "shall",
            "should",
            "can",
            "could",
            "may",
            "might",
            "must",
            "ought",
            "i'm",
            "you're",
            "he's",
            "she's",
            "it's",
            "we're",
            "they're",
            "i've",
            "you've",
            "we've",
            "they've",
            "i'd",
            "you'd",
            "he'd",
            "she'd",
            "we'd",
            "they'd",
            "i'll",
            "you'll",
            "he'll",
            "she'll",
            "we'll",
            "they'll",
            "isn't",
            "aren't",
            "wasn't",
            "weren't",
            "hasn't",
            "haven't",
            "hadn't",
            "doesn't",
            "don't",
            "didn't",
            "won't",
            "wouldn't",
            "shan't",
            "shouldn't",
            "can't",
            "cannot",
            "couldn't",
            "mustn't",
            "let's",
            "that's",
            "who's",
            "what's",
            "here's",
            "there's",
            "when's",
            "where's",
            "why's",
            "how's",
            "daren't",
            "needn't",
            "oughtn't ",
            "mightn't",
            "a",
            "an",
            "the",
            "and",
            "but",
            "if",
            "or",
            "because",
            "as",
            "until",
            "while",
            "of",
            "at",
            "by",
            "for",
            "with",
            "about",
            "against",
            "between",
            "into",
            "through",
            "during",
            "before",
            "after",
            "above",
            "below",
            "to",
            "from",
            "up",
            "down",
            "in",
            "out",
            "on",
            "off",
            "over",
            "under",
            "again",
            "then",
            "once",
            "here",
            "there",
            "when",
            "where",
            "why",
            "how",
            "all",
            "any",
            "both",
            "each",
            "few",
            "more",
            "most",
            "other",
            "some",
            "such",
            "no",
            "nor",
            "not",
            "only",
            "own",
            "same",
            "so",
            "than",
            "too",
            "very",
            "ever",
            "also",
            "just",
            "whether",
            "like",
            "even",
            "still",
            "since",
            "another",
            "however",
            "please",
            "much",
            "many"]

pattern = r"""(?x)                   # set flag to allow verbose regexps 
              (?:[A-Z]\.)+           # abbreviations, e.g. U.S.A. 
              |\d+(?:\.\d+)?%?       # numbers, incl. currency and percentages 
              |\w+(?:[-']\w+)*       # words w/ optional internal hyphens/apostrophe 
              |\.\.\.                # ellipsis 
              |(?:[.,;"'?():-_`])    # special characters with meanings 
            """  

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle') 
# wordtokenizer = RegexpTokenizer(pattern)
lemmatizer = WordNetLemmatizer()

codePattern = re.compile(r'<code>([\s\S]*?)</code>', re.I)

def isDelete(word):
    if word in stop_word:
        return True
    if not re.match('.*[a-zA-Z]+.*', word, re.I):
        return True
    return False        


def preprocess(paragraph):
    result = []
    sentences = tokenizer.tokenize(paragraph.lower())
    for sentence in sentences:
        words = nltk.regexp_tokenize(sentence, pattern) 
        temp = []
        for word in words:
            if not isDelete(word):
                temp.append(lemmatizer.lemmatize(word))
        result.append(temp)
    return result

def processHTML(html):
      codes = codePattern.findall(html, re.I)
      texts = re.sub(r'(<pre>\s*?<code>[\s\S]*?</code>\s*?</pre>)', '', html, 0, re.I)
      texts = re.sub(r'(<.*?>)', '', texts, 0, re.I)
      texts = re.sub(r'(</.*?>)', '', texts, 0, re.I)
      return (codes, texts)

if __name__ == '__main__':
    print processHTML('''Examples shown in the javadoc for <code>ReplayingDecoder</code> seems to be wrong. In the document it shows <code>IntegerHeaderFrameDecoder, MyDecoder</code> taking multiple parameters where as in reality it can only accept one. I'm working with versions 4.0.0.CR3, 4.0.0.CR5.
 
 ''')
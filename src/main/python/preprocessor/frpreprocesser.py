# -*- coding: UTF-8 -*-

import re
import nltk
import nltk.data
import nltk.stem

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

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
stemmer = nltk.stem.SnowballStemmer('english')

notationP = re.compile(r'([A-Za-z]+[0-9]*_.*)')
qualifiedP = re.compile(r'([A-Za-z]+[0-9]*[\.].+)')
camelP = re.compile(r'([A-Za-z]+.*[A-Z]+.*)')
upperP = re.compile(r'([A-Z0-9]+)')
systemP = re.compile(r'(_+[A-Za-z0-9]+.+)')
referenceP = re.compile(r'([a-zA-Z]+[:]{2}.+)')


def isDelete(word):
    if word in stop_word:
        return True
    if not re.match('.*[a-zA-Z]+.*', word, re.I):
        return True
    return False


def extractCode(text):
    text = re.sub(r'(\[[\s\S]*?\])', '', text, 0, re.I)
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '',
                  text, 0, re.I)
    result = []
    words = text.split()
    for word in words:
        result.extend(dealWord(word))
    return result


def splitCamel(code):
    res = []
    words = re.split(r"([A-Z]+[a-z]*)", code)
    for word in words:
        if word:
            res.append(word)
    return res


def dealWord(word):
    result = []
    if notationP.match(word) or qualifiedP.match(word) or camelP.match(word) or upperP.match(word) or systemP.match(word) or referenceP.match(word):
        parts = nltk.word_tokenize(word)
        for part in parts:
            if not isDelete(part.lower()):
                result.append(stemmer.stem(part.lower()))
    return result


def extractText(text):
    text = re.sub(r'(\[[\s\S]*?\])', '', text, 0, re.I)
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '',
                  text, 0, re.I)
    result = []
    words = nltk.word_tokenize(text)
    for word in words:
        if not isDelete(word.lower()):
            result.append(stemmer.stem(word.lower()))
    return result


if __name__ == '__main__':
    print extractCode("[beam-213] I performed the tests, but he left me too bad.")
#     print stemmer.stem('has')
#     print stemmer.stem('have')
#     print splitCamel("CodeIndex")
#     print splitCamel("codeIndex")
    print extractText('''
   print() is a function in Python 3DESCRIPTION HERE `test.test()`\r\n\r\n------------------------\r\n\r\nFollow this checklist to help us incorporate your contribution quickly and easily:\r\n\r\n - [ ] Make sure there is a [JIRA issue](https://issues.apache.org/jira/projects/BEAM/issues/) filed for the change (usually before you start working on it).  Trivial changes like typos do not require a JIRA issue.  Your pull request should address just this issue, without pulling in other changes.\r\n - [ ] Format the pull request title like `[BEAM-XXX] Fixes bug in ApproximateQuantiles`, where you replace `BEAM-XXX` with the appropriate JIRA issue.\r\n - [ ] Write a pull request description that is detailed enough to understand:\r\n   - [ ] What the pull request does\r\n   - [ ] Why it does it\r\n   - [ ] How it does it\r\n   - [ ] Why this approach\r\n - [ ] Each commit in the pull request should have a meaningful subject line and body.\r\n - [ ] Run `mvn clean verify` to make sure basic checks pass. A more thorough check will be performed on your pull request automatically.\r\n - [ ] If this contribution is large, please file an Apache [Individual Contributor License Agreement](https://www.apache.org/licenses/icla.pdf).\r\n\r\n
OPT_INFO_TEST testtest is OperaTest COR _cmdline std::env
     ''')

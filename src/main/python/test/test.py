# -*- coding: UTF-8 -*-

from gitresolver import gitResolver
from preprocessor import preprocessor
import datetime

# ioHandler.buildCorpus("model.dat", "corpus.dat")
path = 'D:/github/checkstyle'
repo = gitResolver.GitResolver(path)

def getDiffday(date1, date2):
    return abs((date1-date2).days)

commit = repo.getCommits()[0]
diffs = repo.getOneDiff(commit)
print preprocessor.preprocess("I like it.\n\n\n\nI love it. I hate it.")
print str(repo.getDateTime(commit))
print getDiffday(repo.getDateTime(commit), datetime.datetime.now())
print commit.hexsha.encode("utf-8")
print type(commit.hexsha.encode("utf-8"))
print repo.getOneCommit(str(commit.hexsha.encode("utf-8"))).message
for diff in diffs:
    print diff.diff
#     print diff.a_blob.data_stream.read().decode('utf-8')
#     print diff.b_blob.data_stream.read().decode('utf-8')
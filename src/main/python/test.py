# -*- coding: UTF-8 -*-

from preprocessor import ioHandler
from gitresolver import gitResolver

# ioHandler.buildCorpus("model.dat", "corpus.dat")
path = 'D:/github/checkstyle'
repo = gitResolver.GitResolver(path)

commit = repo.getCommits()[0]
diffs = repo.getOneDiff(commit)
print commit.message
print repo.getCommitDate(commit)
    
    # if diff.change_type == 'M':
    #     print diff.a_blob.data_stream.read().decode('utf-8'),"\n"
    #     print diff.b_blob.data_stream.read().decode('utf-8'),"\n"
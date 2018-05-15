# -*- coding: UTF-8 -*-

from gitresolver import gitResolver
import datetime

# ioHandler.buildCorpus("model.dat", "corpus.dat")
path = 'D:/github/gocd'
repo = gitResolver.GitResolver(path)
commits = repo.getCommits()

oneCommit = repo.getOneCommit('af958acc95e246462541866773b8f91eead069d9')

print oneCommit in commits
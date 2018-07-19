# -*- coding: UTF-8 -*-

from gitresolver import gitResolver
import datetime

# ioHandler.buildCorpus("model.dat", "corpus.dat")
path = 'D:/github/gocd'
repo = gitResolver.GitResolver(path)

print repo.getFiles('e3d55a8f99712a8d447ce3d30025340d52b5e254')

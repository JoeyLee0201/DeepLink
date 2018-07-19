# -*- coding: UTF-8 -*-

from gitresolver import gitResolver
import datetime

# ioHandler.buildCorpus("model.dat", "corpus.dat")
path = 'D:/github/checkstyle'
repo = gitResolver.GitResolver(path)

# print repo.getFiles('76d6365018ec7688c8a8475b2f9aa496fbcfe88c')
print repo.getFiles('eceaa8b65a982db58d31ac901cdd751c435b1362')

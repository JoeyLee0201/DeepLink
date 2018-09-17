# -*- coding: UTF-8 -*-
import os
import json
from preprocessor import preprocessor


def read_data(name, repoId):
    filepath = os.path.join("./train%d" % repoId, name)
    file = open(filepath, 'rb')
    testlist = json.loads(file.read())
    file.close()
    return testlist


def main(repoId, i):
    # filename = raw_input('**Please input the file name:')
    filename = "traincase%d-%d.dat" % (repoId, i)
    mapList = read_data(filename, repoId)
    print '\033[1;33;0m', filename, ':', len(mapList), '\033[0m'
    index = 0
    while True:
        print '\033[1;33;0m====================================================================================================\033[0m'
        # index = int(raw_input('**Please input the index:'))
        goOn = int(raw_input('** continue?'))
        if goOn == 0:
            return
        print '\033[1;31;0m----[', mapList[index]['type'], ']----\033[0m'
        print '\033[1;31;0m--------commit--------\033[0m'
        print mapList[index]['commit']
        print preprocessor.preprocessNoCamel(mapList[index]['commit'])
        print '\033[1;31;0m--------title--------\033[0m'
        print mapList[index]['issuetitle']
        print preprocessor.preprocessNoCamel(mapList[index]['issuetitle'])
        print '\033[1;31;0m--------issue body--------\033[0m'
        print '\033[4;32;0m', mapList[index]['issue'], '\033[0m'
        print preprocessor.processHTMLNoCamel(mapList[index]['issue'])
        index = index + 1


if __name__ == "__main__":
    main(18845024, 2)

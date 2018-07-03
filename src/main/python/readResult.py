# -*- coding: UTF-8 -*-
import os
import json
from preprocessor import preprocessor


def read_data(name):
    filepath = os.path.join('./fiveTest', name)
    file = open(filepath, 'rb')
    testlist = json.loads(file.read())
    file.close()
    return testlist


def main(filename):
    # filename = raw_input('**Please input the file name:')
    mapList = read_data(filename)
    print '\033[1;33;0m', filename, ':', len(mapList), '\033[0m'
    while True:
        print '\033[1;33;0m====================================================================================================\033[0m'
        index = int(raw_input('**Please input the index:'))
        if index < 0:
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



if __name__ == "__main__":
    main('traincase12499251-8.dat')
    # main('traincase13421878-8.dat')
    # main('traincase20587599-5.dat')
    # main('traincase27729926-5.dat')
    # main('traincase50904245-6.dat')

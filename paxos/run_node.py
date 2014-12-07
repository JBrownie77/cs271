#!/usr/bin/python

'''
Created on Dec 5, 2014

@author: Karthik Puthraya
'''
from sys import argv
from node import Node
from time import sleep

if __name__ == '__main__':
    if len(argv) == 3:
        print 'Starting server at port {0}'.format(argv[2])
        n = Node(argv[1], int(argv[2]))
        n.start()
        while True:
            try: 
                print n.paxosStates[0]
            except:
                pass
            sleep(5)
    elif len(argv) == 4:
        print 'Starting server at port {0}'.format(argv[2])
        n = Node(argv[1], int(argv[2]))
        n.start()
        print 'Starting Paxos with value {0}'.format(argv[3])
        n.initPaxos(0, value = argv[3])
        while True:
            try: 
                print n.paxosStates[0]
            except:
                pass
            sleep(5)


    
    
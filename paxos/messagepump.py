'''
Created on Dec 3, 2014
@author: Karthik Puthraya
'''

import threading
import Queue
import sys
import socket
import time

class MessagePump(threading.Thread):
    '''
    This class listens to a port on a node and passes the messages it receives to
    the main thread.
    '''
    
    def __init__(self, queue, msgReceived, owner = None, ip = None, port = 55555):
        '''
        The MessagePump binds itself to port and appends all the messages it receives
        to a queue
        '''
        threading.Thread.__init__(self)
        self.owner = owner
        if ip == None:
            self.ip = socket.gethostbyname(socket.gethostname())
            print socket.gethostbyname(socket.gethostname())
        else:
            self.ip = ip
        self.port = port
        self.queue = queue
        self.msgReceived = msgReceived
        self.socket = None
        self.isRunning = True
    
    def run(self):
        print 'Starting message pump and listening to {0}:{1}'.format(self.ip, self.port)

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind((self.ip, self.port))
            self.isRunning = True
        
            #self.socket.settimeout( timeout )
        
        except Exception as e:
            if self.socket:
                self.socket.close()
            
            print 'Could not open/bind to socket.'
            print 'Exception message: ', e
            sys.exit(1)
        
        # Listen forever on the port and add received messages to the queue
        while True:
                data, addr = self.socket.recvfrom(4096)
                if self.isRunning:
                    self.queue.put((data, addr))
                    self.msgReceived.set()
    
if __name__ == '__main__':
    queue = Queue.Queue()
    msgReceived = threading.Event()
    msgReceived.clear()
    
    mp = MessagePump(queue, msgReceived)
    mp.setDaemon(True)
    mp.start()
    
    while True:
        msgReceived.wait()
        if not queue.empty():
            data, addr = queue.get()
            print addr, data
        msgReceived.clear()
    
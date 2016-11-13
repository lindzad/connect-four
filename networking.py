import socket
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor


class Echo(DatagramProtocol):
    def datagramReceived(self, data, addr):
        print("received %r from %s" % (data, addr))
        self.transport.write(data, addr)

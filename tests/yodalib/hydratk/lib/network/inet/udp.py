import socket
import sys


class Server(object):

    def start(self, host='127.0.0.1', port=10000):

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        server_address = ('localhost', 10000)
        print >>sys.stderr, 'starting up on %s port %s' % server_address
        sock.bind(server_address)

        while True:
            print >>sys.stderr, '\nwaiting to receive message'
            data, address = sock.recvfrom(4096)

            print >>sys.stderr, 'received %s bytes from %s' % (
                len(data), address)
            print >>sys.stderr, data

            if data:
                sent = sock.sendto(data, address)
                print >>sys.stderr, 'sent %s bytes back to %s' % (
                    sent, address)

from tftpy import TftpServer


class Server(object):

    _server = None
    _ip = None
    _port = None
    _path = None

    def __init__(self, path='/var/local/hydratk'):

        self._server = TftpServer(tftproot=path)
        self._path = path

    def start(self, ip='127.0.0.1', port=69, timeout=10):

        self._server.listen(ip, port, timeout)
        self._ip = ip
        self._port = port

    def stop(self):

        self._server.stop()

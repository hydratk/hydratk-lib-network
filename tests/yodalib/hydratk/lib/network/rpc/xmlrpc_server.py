from SimpleXMLRPCServer import SimpleXMLRPCServer


class Server(object):

    _server = None
    _ip = None
    _port = None

    def __init__(self, ip='127.0.0.1', port=8000):

        self._ip = ip
        self._port = port
        self._server = SimpleXMLRPCServer(
            (self._ip, self._port), allow_none=True)
        self.register()

    def register(self):

        self._server.register_multicall_functions()
        self._server.register_function(self._callRemote, 'callRemote')
        self._server.register_function(self._out_int, 'out_int')
        self._server.register_function(self._out_string, 'out_string')
        self._server.register_function(self._in_int, 'in_int')
        self._server.register_function(self._in_string, 'in_string')
        self._server.register_function(self._in2, 'in2')

    def start(self):

        self._server.serve_forever()

    def _callRemote(self):

        print('Method has been called!!!!')

    def _out_int(self):

        return 666

    def _out_string(self):

        return 'Sucker'

    def _in_int(self, i):

        print(i)
        return i + 6

    def _in_string(self, s):

        print(s)
        return s + ' xxx'

    def _in2(self, i1, i2):

        return str(i1) + str(i2)

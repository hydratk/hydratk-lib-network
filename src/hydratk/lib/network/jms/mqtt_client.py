# -*- coding: utf-8 -*-
"""MQTT client

.. module:: network.jms.mqtt_client
   :platform: Unix
   :synopsis: MQTT client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
jms_before_connect
jms_after_connect
jms_before_send
jms_after_send
jms_before_receive
jms_after_receive

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from paho.mqtt.client import Client
from paho.mqtt import MQTTException
from socket import error, setdefaulttimeout
from time import time


class JMSClient(object):
    """Class JMSClient
    """

    _mh = None
    _client = None
    _host = None
    _port = None
    _user = None
    _passw = None
    _verbose = None
    _is_connected = None
    _messages = []

    def __init__(self, verbose=False):
        """Class constructor

        Called when the object is initialized

        Args:                   
           verbose (bool): verbose mode

        """

        try:

            self._mh = MasterHead.get_head()

            self._client = Client()
            self._client.on_message = self._on_message

            self._verbose = verbose
            if (self._verbose):
                self._client.on_log = self._on_log

        except MQTTException as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())

    @property
    def client(self):
        """ MQTT client property getter """

        return self._client

    @property
    def host(self):
        """ server host property getter """

        return self._host

    @property
    def port(self):
        """ server port property getter """

        return self._port

    @property
    def user(self):
        """ username property getter """

        return self._user

    @property
    def passw(self):
        """ user password property getter """

        return self._passw

    @property
    def verbose(self):
        """ verbose property getter """

        return self._verbose

    @property
    def is_connected(self):
        """ is_connected property getter """

        return self._is_connected

    def _on_log(self, client, obj, level, string):
        """ Callback for on_log event """

        print(string)

    def _on_message(self, client, obj, msg):
        """ Callback for on_message event """

        self._messages.append(msg.payload.decode())

    def connect(self, host, port=1883, user=None, passw=None, timeout=10):
        """Method connects to server

        Args:
           host (str): hostname
           port (str): port
           user (str): username
           passw (str): password
           timeout (int): timeout

        Returns:
           bool: result

        Raises:
           event: jms_before_connect
           event: jms_after_connected            

        """

        try:

            msg = 'host:{0}, port:{1}, user:{2}, passw:{3}, timeout:{4}'.format(
                host, port, user, passw, timeout)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_jms_connecting', msg), self._mh.fromhere())

            ev = event.Event(
                'jms_before_connect', host, port, user, passw, timeout)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                port = ev.argv(1)
                user = ev.argv(2)
                passw = ev.argv(3)
                timeout = ev.argv(4)

            self._host = host
            self._port = port
            self._user = user
            self._passw = passw

            if (ev.will_run_default()):
                if (self._user != None):
                    self._client.username_pw_set(self._user, self._passw)

                setdefaulttimeout(timeout)
                self._client.connect(self._host, self._port)
                self._is_connected = True

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_jms_connected'), self._mh.fromhere())
            ev = event.Event('jms_after_connect')
            self._mh.fire_event(ev)

            return True

        except (MQTTException, error, ValueError) as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return False

    def disconnect(self):
        """Method disconnects from server 

        Args:   
           none       

        Returns:
           bool: result

        """

        try:

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_jms_disconnecting'), self._mh.fromhere())

            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg(
                    'htk_jms_not_connected'), self._mh.fromhere())
                return False
            else:
                self._client.disconnect()
                self._is_connected = False
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                    'htk_jms_disconnected'), self._mh.fromhere())
                return True

        except (MQTTException, error, ValueError) as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return False

    def send(self, destination_name, message):
        """Method sends message

        Args:
           destination_name (str): topic name
           message (str): message

        Returns:
           bool: result

        Raises:
           event: jms_before_send
           event: jms_after_send             

        """

        try:

            msg = 'destination_name:{0}, message:{1}'.format(
                destination_name, message)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_jms_sending_msg', msg), self._mh.fromhere())

            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg(
                    'htk_jms_not_connected'), self._mh.fromhere())
                return False

            ev = event.Event('jms_before_send', destination_name, message)
            if (self._mh.fire_event(ev) > 0):
                destination_name = ev.argv(0)
                message = ev.argv(1)

            if (ev.will_run_default()):
                res, id = self._client.publish(destination_name, message)

                if (res != 0):
                    self._mh.dmsg('htk_on_error', self._mh._trn.msg(
                        'htk_jms_sending_error'), self._mh.fromhere())

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_jms_msg_sent'), self._mh.fromhere())
            ev = event.Event('jms_after_send')
            self._mh.fire_event(ev)

            return True

        except (MQTTException, error, ValueError) as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return False

    def receive(self, destination_name, cnt=1, timeout=10):
        """Method receives messages

        Args:
           destination_name (str): queue name
           cnt (int): count of messages
           timeout (int): timeout to receive message

        Returns:
           list:  messages

        Raises:
           event: jms_before_receive
           event: jms_after_receive             

        """

        try:

            msg = 'destination_name:{0}, count:{1}'.format(
                destination_name, cnt)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_jms_receiving_msg', msg), self._mh.fromhere())

            if (not self._is_connected):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg(
                    'htk_jms_not_connected'), self._mh.fromhere())
                return None

            ev = event.Event('jms_before_receive', destination_name, cnt)
            if (self._mh.fire_event(ev) > 0):
                destination_name = ev.argv(0)
                cnt = ev.argv(1)

            if (ev.will_run_default()):
                res, id = self._client.subscribe(destination_name)
                if (res != 0):
                    self._mh.dmsg('htk_on_error', self._mh._trn.msg(
                        'htk_jms_sending_error'), self._mh.fromhere())
                    return None

                res = 0
                cnt_before = 0
                start = time()
                while (res == 0):
                    res = self._client.loop()
                    cnt_after = len(self._messages)
                    if (cnt_after > cnt_before and cnt_after < cnt):
                        cnt_before = cnt_after
                    elif (cnt_after == cnt or time() > start + timeout):
                        res = -1

                messages = self._messages
                self._client.unsubscribe(destination_name)
                self._messages = []

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg(
                'htk_jms_msg_received', len(messages)), self._mh.fromhere())
            ev = event.Event('jms_after_receive')
            self._mh.fire_event(ev)

            return messages

        except (MQTTException, error, ValueError) as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None

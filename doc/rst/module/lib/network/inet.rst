.. _module_lib_network_inet:

INET
====

This sections contains module documentation of inet module.

client
^^^^^^

Module provides class Client for TCP and UDP client using Python module 
`socket <https://docs.python.org/3.6/library/socket.html>`_.
Unit tests available at hydratk/lib/network/inet/client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _lay3_prot - 3rd layer protocol (IPV4, IPV6)
* _lay4_prot - 4th layer protocol (TCP, UDP)
* _client - ftplib client instance
* _host - server hostname (or IP address)
* _port - port number
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.

**Properties (Getters)** :

* client - returns _client
* lay3_prot - returns _lay3_prot
* lay4_prot - returns _lay4_prot
* host - returns _host
* port - returns _port
* is_connected - returns _is_connected

**Methods** :

* __init__

Sets _client to socket instance (constructor secure). Parameters lay3_prot, lay4_prot must be supported, otherwise NotImplementedError is raised.

  .. code-block:: python
  
     from hydratk.lib.network.inet.client import Client
  
     # TCP over IPv6
     c1 = Client('IPV6', 'TCP')
     
     # UDP over IPv4
     c2 = Client('IPV4', 'UDP')

* connect

Connects to server (specified via parameters host, port). Only TCP supports connection, UDP is connectionless protocol.
First fires event inet_before_connect where parameters can be rewritten. Connects to server using method socket method connect.
After successful connection fires event inet_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     res = c1.connect(host='127.0.0.1', port=22)
     
* disconnect

Disconnects from database using socket method close (and shutdown for TCP) and returns bool.

  .. code-block:: python
  
     res = c1.disconnect()     
     
* send

Sends data to server (specified via parameters data, host, port). host and port are intended for UDP because connection is not established.
First fires event inet_before_send where parameters can be rewritten. Sends data using socket method sendall for TCP and sendto for UDP.
After that fires event inet_after_send and returns bool.

  .. code-block:: python
  
     # TCP
     res = c1.send('I am Hydra')     
     
     # UDP
     res = c2.send('I am Hydra', '127.0.0.1', 10000)  
     
* receive

Receives data from server. First fires event inet_before_receive where parameters (size, timeout) can be rewritten. 
Receives data using socket method recv for TCP and recvfrom for UDP, default size is 4096 bytes. Timeout is 10s by default (parameter timeout).
After that fires event inet_after_receive and returns data.

  .. code-block:: python
  
     res = c.receive()
     
* ip2name

Translates IP address to DSN name using socket method gethostbyaddr.

  .. code-block:: python
  
     res = c.ip2name('127.0.0.1')

* name2ip

Translates DSN name to IP address using socket method getaddrinfo.  

  .. code-block:: python
  
     res = c.name2ip('localhost')         
     
packet
^^^^^^

Module provides packets method using external module 
`scapy <http://www.secdev.org/projects/scapy/doc/usage.html>`_. in version >= 2.3.1.
When Python3 is used scapy is replaced by module `scapy-python3 <https://github.com/phaethon/scapy>` in version >= 0.18.

Unit tests available at hydratk/lib/network/inet/packet/01_methods_ut.jedi 
The module usually requires root privileges (required by module socket when working with non-standard packets).

**Methods** :

* Packet

Initializes packet of any supported protocol (see scapy documentation) using scapy constructor. 
Parameters are passed as kwargs. Raises NotImplementedError when protocol is not supported.

  .. code-block:: python
  
     from hydratk.lib.network.inet.packet import Packet
     
     p = Packet('Ether')
     p = Packet('IP', dst='google.com')
     p = Packet('TCP', dport=80)     
     
* compose_packet 

Prepares compound packet possibly with payload.

  .. code-block:: python
  
     from hydratk.lib.network.inet.packet import compose_packet, Packet
  
     # two packets
     p = [Packet('IP', dst='google.com'), Packet('TCP', dport=80)]
     c = compose_packet(p)    
     
     # packet with payload
     c = compose_packet(p, 'test') 
     
* dump

Prints packet content in human readable or hexdump (if parameter raw=True) form. Using scapy methods show or hexdump.

  .. code-block:: python     
  
     from hydratk.lib.network.inet.packet import Packet, dump
     
     p = Packet('IP', dst='google.com')
     
     # human readable
     dump(p, False)
     
     # hexdump
     dump(p, True)
     
* send_packet
   
Sends packet. First fires event inet_before_send_packet where parameters (packet, iface, verbose) can be rewritten.   
Sends packet using scapy method send or sendp (when iface is provided). After that fires event inet_after_send_packet.

  .. code-block:: python
  
     from hydratk.lib.network.inet.packet import Packet, compose_packet, send_packet
     
     p = [Packet('IP', dst='127.0.0.1'), Packet('TCP', dport=22)] 
     pck = compose_packet(p, 'I am Hydra')
     
     # default iface
     send_packet(pck)
     
     # given iface
     send_packet(pck, iface='eth1')
     
* send_recv_packet
   
Sends packet and receives answer. First fires event inet_before_sendrecv_packet where parameters (packet, iface, retry, timeout, verbose) can be rewritten.   
Sends packet using scapy method sr or srp (when iface is provided). After that fires event inet_after_sendrecv_packet and returns tuple of packets (answered, unanswered).

  .. code-block:: python
  
     from hydratk.lib.network.inet.packet import Packet, compose_packet, send_recv_packet
     
     p = [Packet('IP', dst='google.com'), Packet('TCP', dport=80)] 
     pck = compose_packet(p, 'I am Hydra')      
     
     # default iface
     ans, unans = send_recv_packet(pck)
     
     # given iface
     ans, unans = send_recv_packet(pck, iface='eth1')
     
* ping

Pings given host. First fires event inet_before_ping where parameters (destination, protocol, port, verbose) can be rewritten.
Methods prepares necessary packets and send them. ICMP protocol is used by default. TCP ping is emulated via connection to given port. 
After that fires event inet_after_ping and returns bool.

  .. code-block:: python
  
     from hydratk.lib.network.inet.packet import ping
     
     # ICMP
     res = ping('google.com', 'ICMP')
     
     # TCP
     res = ping('google.com', 'TCP', 80)
     
* traceroute

Traceroutes given host. First fires event inet_before_traceroute where parameters (destination, protocol, port, max_hops, verbose) can be rewritten.
Methods prepares necessary packets and sends them. ICMP protocol is used by default. TCP ping is emulated via connection to given port. 
Result is parsed from answered packets. After that fires event inet_after_traceroute and returns bool. Traceroute path is printed.

  .. code-block:: python
  
     from hydratk.lib.network.inet.packet import traceroute
     
     # ICMP
     res = traceroute('google.com', 'ICMP')
     
     # TCP
     res = traceroute('google.com', 'TCP', 80)     
     
* sniffer

Sniffer network traffic. First fires event inet_before_sniff where parameters (output, iface, filter, timeout) can be rewritten.
filter uses special syntax format, see scapy documentation. Methods sniffs traffic using scapy method sniff and writes content to pcap 
file using scapy method wrpcap. After that fires event inet_after_sniff.

  .. code-block:: python
  
     from hydratk.lib.network.inet.packet import sniffer
     
     # all ifaces
     file = '/var/local/hydratk/test.pcap'
     sniffer(file)
     
     # given iface
     sniffer(file, iface='eth0') 
     
     # traffic filter
     sniffer(file, filter='icmp and host google.com')      
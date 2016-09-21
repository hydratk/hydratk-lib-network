.. _tutor_network_tut4_inet:

Tutorial 4: INET
================

This sections shows several examples how to use INET client and packet methods.

API
^^^

Module hydratk.lib.network.inet.client

methods:

* connect: connect to server
* disconnect: disconnect from server
* send: send data to server
* receive: receive data from server
* ip2name: resolve IP address to DNS name
* name2ip: resolve DNS name to IP address

Module hydratk.lib.network.inet.packet

methods:

* Packet: factory method to create packet for required protocol
* compose_packet: compose complete packet from packets for partial protocols 
* dump: print packet dump
* send_packet: send packet to server
* send_recv_packet: send packet to server and receive answer
* ping: ping server
* traceroute: traceroute server
* sniffer: sniff network traffic

  .. note::
   
     API uses HydraTK core functionalities so it must be running.

TCP
^^^

  .. code-block:: python
    
     # import library
     from hydratk.lib.network.inet.client import Client
     
     # initialize client
     client = inet.Client('IPv4', 'TCP')   
     
     # connect to server
     # returns bool
     client.connect('lxbillppt402.ux.to2cz.cz', 22)  
     
     # send data
     client.send('I am hydra') 
     
     # receive data
     client.receive() 
     
     # resolve IP address <-> DNS name
     print client.name2ip('lxbillppt402.ux.to2cz.cz')  
     print client.ip2name('172.26.128.24')
     
     # disconnect from server
     # returns bool
     client.disconnect() 
   
UDP  
^^^   

  .. code-block:: python
    
     # import library
     from hydratk.lib.network.inet.client import Client
     
     # initialize client
     client = inet.Client('IPv4', 'UDP')
     
     # send data
     # server must be provided because UDP is connection-less protocol
     client.send('I am hydra', 'lxbillppt402.ux.to2cz.cz', 22)
     
     # receive data, wait 10 seconds
     client.receive(timeout=10)  
     
Packet
^^^^^^

  .. code-block:: python   
  
     # import library
     import hydratk.lib.network.inet.packet as inet  
     
     # prepare compound packet from Ether, IP, TCP protocols
     packets = [inet.Packet('Ether'), inet.Packet('IP', dst='google.com'), inet.Packet('TCP', dport=80)]
     packet = inet.compose_packet(packets, '123456789123456789')
     
     # print packet
     inet.dump(packet)
     
     # send packet via eth0 interface    
     inet.send_packet(packets, iface='eth0')       
     
     # send packet and receive answer 
     inet.send_recv_packet(packet, iface='eth0') 
     
     # ping server via ICMP, TCP
     inet.ping('google.com', 'ICMP')  
     inet.ping('google.com', 'TCP', 80)   
     
     # traceroute server via ICMP, TCP
     inet.traceroute('google.com', 'ICMP')
     inet.traceroute('google.com', 'TCP', 80)
     
     # sniff network traffic and store it to pcap file
     inet.sniffer('./mine.pcap')    
     
  .. note::
  
     These methods must be executed with admin rights otherwise permission required error is raised.
     Library uses raw packets from module socket.     
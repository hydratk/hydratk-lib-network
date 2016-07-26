# -*- coding: utf-8 -*-
"""Raw packet networking

.. module:: network.inet.packet
   :platform: Unix
   :synopsis: Raw packet networking
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
inet_before_send_packet
inet_after_send_packet
inet_before_sendrecv_packet
inet_after_sendrecv_packet
inet_before_ping
inet_after_ping
inet_before_traceroute
inet_after_traceroute
inet_before_sniff
inet_after_sniff

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from hydratk.lib.network.inet.client import Client
from logging import getLogger, ERROR
from socket import error
from importlib import import_module

getLogger('scapy.runtime').setLevel(ERROR)

from scapy.error import Scapy_Exception

mh = MasterHead.get_head()

def Packet(protocol, **kwargs):
    """Packet factory method
        
    Whole scapy protocol stack is supported    
        
    Args:            
       protocol (str): protocol
       kwargs (kwargs): key value arguments 
           
    Returns:
       obj: Packet
        
    Raises:
       error: NotImplementedError
                
    """       
    
    try:
        
        mod = import_module('scapy.all')
        packet = mod.__dict__[protocol](**kwargs)
        mh.find_module('hydratk.lib.network.inet.packet', None)   
                        
        return packet
    
    except KeyError as ex:
        
        raise NotImplementedError('Unknown protocol: {0}'.format(protocol))        

def compose_packet(packets, payload=None):
    """Method composes packet from partial packets
        
    Args:            
       packets (list): partial packets
       payload (str): packet payload
           
    Returns:
       obj: Packet
                
    """       
    
    try:
    
        if (len(packets) > 0):
            packet = packets[0]
        
            for pak in packets[1:]:
                packet = packet/pak
         
            if (payload != None):
                packet = packet/payload
         
            return packet
    
        else:
            return None
        
    except Scapy_Exception as ex:
        mh.dmsg('htk_on_error', ex, mh.fromhere())
        return None 

def dump(packet, raw=False):
    """Method print packet dump
        
    Args:            
       packet (obj): packet, partial of composed
       raw (bool): print raw hexdump
        
    Returns:
       void
                
    """       
    
    try:        
        
        if (not raw):
            packet.show()
        else:
            from scapy.all import hexdump
            hexdump(packet)            
        
    except Scapy_Exception as ex:
        mh.dmsg('htk_on_error', ex, mh.fromhere())
        return None         

def send_packet(packet, iface=None, verbose=False):
    """Method sends packet
        
    Args:            
       packet (obj): packet
       iface (str): interface, used when Ether packet is included
       verbose (bool): verbose mode
       
    Returns:
       void
        
    Raises:
        event: inet_before_send_packet
        event: inet_after_send_packet
                
    """       
    
    try:    
    
        from scapy.all import send, sendp
        
        mh.dmsg('htk_on_debug_info', mh._trn.msg('htk_inet_sending_packet', iface), mh.fromhere())

        ev = event.Event('inet_before_send_packet', iface, verbose)
        if (mh.fire_event(ev) > 0):
            iface = ev.argv(0)
            verbose = ev.argv(1)

        if (ev.will_run_default()):
            if (iface != None):
                sendp(packet, iface=iface, verbose=verbose)
            else:
                send(packet, verbose=verbose) 
         
        mh.dmsg('htk_on_debug_info', mh._trn.msg('htk_inet_packet_sent'), mh.fromhere()) 
        ev = event.Event('inet_after_send_packet')
        mh.fire_event(ev)          
            
    except (Scapy_Exception, error) as ex:
        mh.dmsg('htk_on_error', ex, mh.fromhere())           
        
def send_recv_packet(packet, iface=None, retry=3, timeout=1, verbose=False):
    """Method sends packet and receives answer
        
    Args:            
       packet (obj): packet
       iface (str): interface, used when Ether packet is included
       retry (int): number of retries
       timeout (int): timeout to receive answer
       verbose (bool): verbose mode
        
    Returns:
        tuple: answered packets, unswered packets
        
    Raises:
        event: inet_before_sendrecv_packet
        event: inet_after_sendrecv_packet
                
    """     
    
    
    try:
        
        from scapy.all import sr, srp      
          
        mh.dmsg('htk_on_debug_info', mh._trn.msg('htk_inet_sending_recv_packet', iface, retry, timeout), 
                mh.fromhere())

        ev = event.Event('inet_before_sendrecv_packet', iface, retry, timeout)
        if (mh.fire_event(ev) > 0):
            iface = ev.argv(0)
            retry = ev.argv(1)
            timeout = ev.argv(2)

        if (ev.will_run_default()):
            if (iface != None):
                ans, unans = srp(packet, iface=iface, retry=retry, timeout=timeout, verbose=verbose)
            else:
                ans, unans = sr(packet, retry=retry, timeout=timeout, verbose=verbose)     
        
        mh.dmsg('htk_on_debug_info', mh._trn.msg('htk_inet_packet_sent_recv'), mh.fromhere())
        ev = event.Event('inet_after_sendrecv_packet')
        mh.fire_event(ev)           
        
        return ans, unans
        
    except (Scapy_Exception, error) as ex:
        return None, None
        mh.dmsg('htk_on_error', ex, mh.fromhere())
    
def ping(destination, protocol='ICMP', port=None, verbose=False):
    """Method executes ping
        
    Args:            
       destination (str): IP address or hostname
       protocol (str): protocol, ICMP|TCP
       port (int): port, used for TCP protocol
       verbose (bool): verbose mode
        
    Returns:
       bool: result
        
    Raises:
       error: ValueError
       event: inet_before_ping
       event: inet_after_ping
                
    """        
    
    try:     
        
        print('ping {0}'.format(destination))
        mh.dmsg('htk_on_debug_info', mh._trn.msg('htk_inet_ping', destination, protocol, port), mh.fromhere())
    
        ev = event.Event('inet_before_ping', destination, protocol, port)
        if (mh.fire_event(ev) > 0):
            destination = ev.argv(0)
            protocol = ev.argv(1)
            port = ev.argv(2)

        if (ev.will_run_default()):            
        
            packets = [Packet('IP', dst=destination)]
            if (protocol == 'ICMP'):
                packets.append(Packet(protocol))
            elif (protocol == 'TCP'):
                packets.append(Packet(protocol, dport=port, flags='S'))
            else:
                raise ValueError('Unknown protocol: {0}'.format(protocol))
        
            packet = compose_packet(packets)
            answers = send_recv_packet(packet, verbose=verbose)[0]                
            
        if (len(answers) > 0 and (protocol == 'ICMP' or hasattr(answers[0][1], 'load'))):
            mh.dmsg('htk_on_debug_info', mh._trn.msg('htk_inet_ping_ok'), mh.fromhere())
            result = True              
        else:
            mh.dmsg('htk_on_debug_info', mh._trn.msg('htk_inet_ping_nok'), mh.fromhere())
            result = False
            
        ev = event.Event('inet_after_ping', result)
        mh.fire_event(ev)             
    
        return result
    
    except Scapy_Exception as ex:
        mh.dmsg('htk_on_error', ex, mh.fromhere()) 
        return False
        
def traceroute(destination, protocol='ICMP', port=None, max_hops=30, verbose=False):  
    """Method executes traceroute
        
    Args:            
       destination (str): IP address or hostname
       protocol (str): protocol, ICMP|TCP
       port (int): port, used for TCP protocol
       max_hops (int): maximum hops
       verbose (bool): verbose mode
        
    Returns:
       bool: result
        
    Raises:
       error: ValueError
       event: inet_before_traceroute
       event: inet_after_traceroute
                
    """         
    
    try:     
        
        print('traceroute {0}'.format(destination))
        mh.dmsg('htk_on_debug_info', mh._trn.msg('htk_inet_traceroute', destination, protocol, port, max_hops), 
                mh.fromhere()) 
        
        ev = event.Event('inet_before_traceroute', destination, protocol, port, max_hops)
        if (mh.fire_event(ev) > 0):
            destination = ev.argv(0)
            protocol = ev.argv(1)
            port = ev.argv(2)
            max_hops = ev.argv(3)

        if (ev.will_run_default()):          
        
            destination = Client().name2ip(destination)
        
            packets = [Packet('IP', dst=destination, ttl=(1, max_hops))]
            if (protocol == 'ICMP'):
                packets.append(Packet(protocol))
            elif (protocol == 'TCP'):
                packets.append(Packet(protocol, dport=port, flags='S'))
            else:
                raise ValueError('Unknown protocol: {0}'.format(protocol))
        
            packet = compose_packet(packets)
            answers = send_recv_packet(packet, verbose=verbose)[0]  
            destination_reached = False
              
        if (len(answers) > 0):
            last_ip = None
            for packet in answers:
                if (packet[1].src != last_ip):
                    last_ip = packet[1].src
                    print('{0}: {1}'.format(packet[0].ttl, last_ip))  
                else:
                    if (last_ip == destination and (protocol == 'ICMP' or hasattr(packet[1], 'load'))):
                        destination_reached = True
                    break;
                
        if (destination_reached):
            mh.dmsg('htk_on_debug_info', mh._trn.msg('htk_inet_traceroute_ok'), mh.fromhere())
            result = True
        else:
            mh.dmsg('htk_on_debug_info', mh._trn.msg('htk_inet_traceroute_nok'), mh.fromhere())   
            result = False    
            
        ev = event.Event('inet_after_traceroute', result)
        mh.fire_event(ev) 
        
        return result                                   
        
    except Scapy_Exception as ex:
        mh.dmsg('htk_on_error', ex, mh.fromhere())   
        return False  
        
def sniffer(output, iface='all', filter=None, timeout=10):   
    """Method executes traffic sniffer
        
    Args:            
       output (str): filename to store packets in PCAP format
       iface (str): interface where traffic will be sniffed, default all interfaces
       filter (str): traffic filter, see scapy doc
       timeout (int): time to stop sniffer
       
    Returns:
       void
        
    Raises:
        event: inet_before_sniff
        event: inet_after_sniff
                
    """         
    
    try:
        
        from scapy.all import sniff, wrpcap
        
        mh.dmsg('htk_on_debug_info', mh._trn.msg('htk_inet_sniffer_started', output, iface, filter, timeout), 
                mh.fromhere())
        
        ev = event.Event('inet_before_sniff', output, iface, filter, timeout)
        if (mh.fire_event(ev) > 0):
            output = ev.argv(0)
            iface = ev.argv(1)
            filter = ev.argv(2)
            timeout = ev.argv(3)

        if (ev.will_run_default()):        
        
            if (iface == 'all'):
                packets = sniff(filter=filter, timeout=timeout)
            else:
                packets = sniff(iface=iface, filter=filter, timeout=timeout)                
        
        if (len(packets) > 0):    
            wrpcap(output, packets) 
         
        mh.dmsg('htk_on_debug_info', mh._trn.msg('htk_inet_sniffer_stopped'), mh.fromhere())            
        ev = event.Event('inet_after_sniff')
        mh.fire_event(ev)             
        
    except (Scapy_Exception, error) as ex:
        mh.dmsg('htk_on_error', ex, mh.fromhere())                  
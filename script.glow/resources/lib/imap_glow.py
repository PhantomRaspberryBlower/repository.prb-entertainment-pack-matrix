#!/bin/python

# UDP multicast examples, Hugo Vincent, 2005-05-14.
import socket, fcntl, struct
import threading

BUFFER_SIZE = 1024
UDP_BROADCAST_IP = '224.1.1.1'
UDP_PORT = 4569

class ImapGlow():

  def send(self, data, port=4569, addr='224.1.1.1'):
    """send(data[, port[, addr]]) - multicasts a UDP datagram."""
    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Make the socket multicast-aware, and set TTL.
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20) # Change TTL (=20) to suit
    # Send the data
    sock.sendto(data, (addr, port))
    sock.close()

  def recv(self, port=4569, multicast_addr='224.1.1.1', buf_size=1024):
    bind_addr = '0.0.0.0'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    membership = socket.inet_aton(multicast_addr) + socket.inet_aton(bind_addr)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((bind_addr, port))
    # Receive the data, then unregister multicast receive membership, then close the port
    sock.settimeout(5.0)
    data, sender_addr = sock.recvfrom(buf_size)
    sock.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton(multicast_addr) + socket.inet_aton('0.0.0.0'))
    sock.close()
    return data, sender_addr[0]

  # Get LAN IP address for either etho or wlan
  def get_lan_ip_addr(self, ifname):
    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      return socket.inet_ntoa(fcntl.ioctl(
          s.fileno(),
          0x8915,  # SIOCGIFADDR
          struct.pack('256s', ifname[:15])
          )[20:24])
    except:
      return 'Error! Unable to get LAN IP address :('

  def get_ip(self):
    # Get current IP address
    lan = self.get_lan_ip_addr('eth0')
    if lan != 'Error! Unable to get LAN IP address :(':
      ip = lan
    else:
      wlan = self.get_lan_ip_addr('wlan0')
      if wlan != 'Error! Unable to get LAN IP address :(':
        ip = wlan
    return ip

  def recv_loop(self, port=4569, addr='224.1.1.1', buf_size=1024):
    current_ip = self.get_ip()
    while True:
      data, sender = self.recv(port, addr, buf_size)
      if sender != current_ip:
        print '%s: %s' % (sender, data)
        return sender, data

#t=threading.Thread(target=recv_loop(UDP_PORT, UDP_BROADCAST_IP, BUFFER_SIZE))
#t.daemon = False
#t.start()
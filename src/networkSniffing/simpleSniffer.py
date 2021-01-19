'''
Created on Apr 15, 2019

@author: rliu01
'''
import socket
import pyshark


s=socket.socket(socket.AF_INET, socket.SOCK_RAW)
# s.bind("192.168.1.151")
# s.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
# s.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)
while True:
 data=s.recvfrom(65565)
 try:
  if "HTTP" in data[0][54:]:
    print "[","="*30,']'
    raw=data[0][54:]
    if "\r\n\r\n" in raw:
     line=raw.split('\r\n\r\n')[0]
     print "[*] Header Captured "
     print line[line.find('HTTP'):]
    else:
     print raw
  else:
   #print '[{}]'.format(data)
   pass
 except:
  pass
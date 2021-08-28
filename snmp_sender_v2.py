from pysnmp.hlapi import *
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.proto import rfc1902
import socket

from pysnmp import debug

# replace the host and port with you host machine and port
host = '127.0.0.1'
port = '1162'
host_name = socket.gethostname()

iterator = sendNotification(
    SnmpEngine(), CommunityData('public', mpModel=0),
    UdpTransportTarget((host, port)), ContextData(), 'trap',
    NotificationType(ObjectIdentity('1.3.6.1.6.3.1.1.5.2')).addVarBinds(
        ('1.3.6.1.2.1.1.1.0',
         OctetString('my system'))).loadMibs('SNMPv2-MIB'))

errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

if errorIndication:
    print(errorIndication)
if errorIndication:
    print('if')
    print(errorIndication)

elif errorStatus:
    print('elif')
    print('%s at %s' %
          (errorStatus.prettyPrint(),
           errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

else:
    print('success')
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))

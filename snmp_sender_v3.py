from pysnmp.hlapi import *
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.proto import rfc1902
import socket

from pysnmp import debug

# replace the host and port with you host machine and port
host = '127.0.0.1'
port = 1163

# replace the credentials as per the environment
username = 'snmp_v3_user'
authkey = 'snmp_v3_authKey'
privkey = 'snmp_v3_privKey'
engine_id = '8000000004030201'

host_name = socket.gethostname()
print('host_name: {}'.format(host_name))

iterator = sendNotification(
    SnmpEngine(OctetString(hexValue=engine_id)),
    UsmUserData(username, authkey, privkey), UdpTransportTarget((host, port)),
    ContextData(), 'trap',
    NotificationType(ObjectIdentity('1.3.6.1.6.3.1.1.5.1')).addVarBinds(
        ('1.3.6.1.2.1.1.1.0', OctetString('my system'))))
errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

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

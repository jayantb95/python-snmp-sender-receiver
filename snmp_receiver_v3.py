# python snmp v3 trap receiver
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import ntfrcv, context
from pysnmp.proto import rfc1902
from datetime import datetime


# replace the credentials as per the environment
engine_id = '8000000004030201'
snmpEngine = engine.SnmpEngine()
snmp_v3_authProtocol = config.usmHMACMD5AuthProtocol
snmp_v3_authKey = 'snmp_v3_authKey'
snmp_v3_privProtocol = config.usmDESPrivProtocol
snmp_v3_privKey = 'snmp_v3_privKey'
snmp_v3_user = 'snmp_v3_user'
snmp_v3_securityEngineId = rfc1902.OctetString(hexValue=engine_id)

# replace the agent and port with you host machine and port
TrapAgentAddress = '127.0.0.1'
Port = 1163

print('Agent is listening SNMP3 Trap on {} , Port : {}'.format(
    TrapAgentAddress, Port))
print(
    '--------------------------------------------------------------------------'
)
config.addTransport(
    snmpEngine, udp.domainName,
    udp.UdpTransport().openServerMode((TrapAgentAddress, Port)))
config.addV3User(snmpEngine, snmp_v3_user, snmp_v3_authProtocol,
                 snmp_v3_authKey, snmp_v3_privProtocol, snmp_v3_privKey,
                 snmp_v3_securityEngineId)


def cbFun(snmpEngine, stateReference, contextEngineId, contextName, varBinds,
          cbCtx):
    print('\n{0}New trap message received on {1} {0}'.format(
        '-' * 20,
        datetime.now().strftime('%d-%b-%Y at %H:%M:%S')))
    print('snmpEngine : {0}'.format(snmpEngine))
    print('stateReference : {0}'.format(stateReference))
    print('contextEngineId : {0}'.format(contextEngineId))
    print('contextName : {0}'.format(contextName))
    print('cbCtx : {0}'.format(cbCtx))
    for name, val in varBinds:
        print('{0} = {1}'.format(name.prettyPrint(), val.prettyPrint()))
    print('{0}Trap message ends{0}\n'.format('-' * 20))


ntfrcv.NotificationReceiver(snmpEngine, cbFun)

snmpEngine.transportDispatcher.jobStarted(1)

try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise
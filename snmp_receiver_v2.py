# python snmp v2 trap receiver
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from datetime import datetime

snmpEngine = engine.SnmpEngine()


# replace the agent and port with you host machine and port
TrapAgentAddress = '127.0.0.1'
Port = 1162

print('Agent is listening SNMP3 Trap on {} , Port : {}'.format(
    TrapAgentAddress, Port))
print(
    '--------------------------------------------------------------------------'
)
config.addTransport(
    snmpEngine, udp.domainName + (1, ),
    udp.UdpTransport().openServerMode((TrapAgentAddress, Port)))

# Configure community here
config.addV1System(snmpEngine, ' ', 'public')


def cbFun(snmpEngine, stateReference, contextEngineId, contextName, varBinds,
          cbCtx):
    print('\n{0}New trap message received on {1} {0}'.format(
        '-' * 20,
        datetime.now().strftime('%d-%b-%Y at %H:%M:%S')))
    print('snmpEngine : {0}'.format(snmpEngine))
    print('stateReference : {0}'.format(stateReference))
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

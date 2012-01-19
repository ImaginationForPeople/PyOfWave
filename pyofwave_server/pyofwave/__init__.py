"""
Starts PyOfWave Server.
"""
import logging

logger = logging.getLogger("pyofwave.server")

def start(settings_mod=None):
    # Setup the configuration using a configuration file
    from conf import setup_environ
    setup_environ(settings_mod)
    
    import storage

    # Initialize data stores
    storage.initialize()

    # Setup Wave Protocol
    import xmpp
    from pyofwave.protocols import WaveProtocol
    # from pyofwave.protocols.wave.wave import WaveOperation
    server = xmpp.XMPPHandler(WaveProtocol)
    #server = xmpp.Server({'plugins': [WaveOperation],
    #                     'host': 'localhost',
    #                      'users': {'user1': 'bob'}
    #                      })
    SP = xmpp.TCPServer(server).bind('127.0.0.1', 5222)
    xmpp.log.setLevel(logging.DEBUG)
    xmpp.start([SP])




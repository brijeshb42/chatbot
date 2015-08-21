import signal
import sys
import getpass
import logging

import sleekxmpp

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


class EchoBot(object):
    """docstring for EchoBot"""
    def __init__(self, jid, password):
        self.xmpp = sleekxmpp.ClientXMPP(jid, password)
        self.xmpp.register_plugin('xep_0030')  # Service Discovery
        self.xmpp.register_plugin('xep_0004')  # Data Forms
        self.xmpp.register_plugin('xep_0060')  # PubSub
        self.xmpp.register_plugin('xep_0199')
        self.xmpp.add_event_handler('session_start', self.handle_connection)
        self.xmpp.add_event_handler('message', self.handle_incoming_msg)

    def run(self):
        logger.info('Connecting...')
        self.xmpp.connect()
        self.xmpp.process(threaded=False)

    def handle_connection(self, event):
        logger.info('Connected to server.')
        self.xmpp.send_presence(pstatus='I am in bot mode.')

    def handle_incoming_msg(self, message):
        logger.info('Message received.')
        self.xmpp.send_message(message['from'], message['body'] + ' lallaal')


def main():
    username = raw_input('Enter JID: ')
    password = getpass.getpass('Enter password: ')
    bot = EchoBot(username+'/scroll.bot', password)
    bot.run()


def signal_handler(signal, frame):
    logger.info('Bye Bye.')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()

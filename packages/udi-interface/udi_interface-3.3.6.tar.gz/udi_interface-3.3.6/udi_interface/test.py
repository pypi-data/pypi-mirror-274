import asyncio
import os
import signal
import time
import ssl
from os.path import exists

from gmqtt import Client as MQTTClient

# gmqtt also compatibility with uvloop
# import uvloop
# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


STOP = asyncio.Event()


def on_connect(client, flags, rc, properties):
    print('Connected')
    client.subscribe('udi/pg3/ns/clients/00:21:b9:02:5f:c2_3', qos=0)


def on_message(client, topic, payload, qos, properties):
    print('RECV MSG:', payload)


def on_disconnect(client, packet, exc=None):
    print('Disconnected')

def on_subscribe(client, mid, qos, properties):
    print('SUBSCRIBED')

def ask_exit(*args):
    STOP.set()

async def main():
    uuid = '00:21:b9:02:5f:c2'
    slot = '3'
    clientId = uuid + '_' + slot
    username = clientId.replace(":", "")
    certpath = '/home/admin/dev/ring/'
    cert = certpath + username + ".cert"
    key = certpath + username + ".key"
    cafilename = '/usr/local/etc/ssl/certs/ud.ca.cert'
    cafile = cafilename if exists(cafilename) else None

    # only if certs exist!
    if not exists(cert):
        print('Missing cert at ' + cert)
    if not exists(key):
        print('Missing key at ' + key)

    print('Using SSL cert: {} key: {} ca: {}'.format(cert, key, cafile))
    sslContext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=cafile)
    sslContext.load_cert_chain(cert, key)

    print('Create client')
    client = MQTTClient(clientId)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe

    print('Connect')
    # client.set_auth_credentials(token, None)
    await client.connect('localhost', port=8883, ssl=sslContext)

    print('Publish')
    client.publish('udi/pg3/ns/custom/' + uuid + '_' + slot, '{"getAll":""}', qos=1)

    print('Stop wait')
    await STOP.wait()
    print('Disconnect')
    await client.disconnect()


if __name__ == '__main__':
    print('Get event loop')
    loop = asyncio.get_event_loop()

    print('Add handlers')
    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)

    print('Run until complete')
    loop.run_until_complete(main())
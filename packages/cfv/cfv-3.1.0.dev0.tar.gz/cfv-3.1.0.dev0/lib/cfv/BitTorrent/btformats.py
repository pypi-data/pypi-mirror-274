# Written by Bram Cohen
# see LICENSE.txt for license information

from re import compile

from builtins import range


reg = compile(br'^[^/\\.~][^/\\]*$')


def check_info(info):
    if type(info) is not dict:
        raise ValueError('bad metainfo - not a dictionary')
    pieces = info.get(b'pieces')
    if type(pieces) is not bytes or len(pieces) % 20 != 0:
        raise ValueError('bad metainfo - bad pieces key')
    piecelength = info.get(b'piece length')
    if type(piecelength) is not int or piecelength <= 0:
        raise ValueError('bad metainfo - illegal piece length')
    name = info.get(b'name')
    if type(name) is not bytes:
        raise ValueError('bad metainfo - bad name')
    if not reg.match(name):
        raise ValueError('name %s disallowed for security reasons' % name)
    if b'files' in info == b'length' in info:
        raise ValueError('single/multiple file mix')
    if b'length' in info:
        length = info.get(b'length')
        if type(length) is not int or length < 0:
            raise ValueError('bad metainfo - bad length')
    else:
        files = info.get(b'files')
        if type(files) is not list:
            raise ValueError
        for f in files:
            if type(f) is not dict:
                raise ValueError('bad metainfo - bad file value')
            length = f.get(b'length')
            if type(length) is not int or length < 0:
                raise ValueError('bad metainfo - bad length')
            path = f.get(b'path')
            if type(path) is not list or path == []:
                raise ValueError('bad metainfo - bad path')
            for p in path:
                if type(p) is not bytes:
                    raise ValueError('bad metainfo - bad path dir')
                if not reg.match(p):
                    raise ValueError('path %s disallowed for security reasons' % p)
        for i in range(len(files)):
            for j in range(i):
                if files[i][b'path'] == files[j][b'path']:
                    raise ValueError('bad metainfo - duplicate path')


def check_message(message):
    if type(message) is not dict:
        raise ValueError
    check_info(message.get(b'info'))
    announce = message.get(b'announce')
    if type(announce) is not bytes or len(announce) == 0:
        raise ValueError('bad torrent file - announce is invalid')


def check_peers(message):
    if type(message) is not dict:
        raise ValueError
    if b'failure reason' in message:
        if type(message[b'failure reason']) is not bytes:
            raise ValueError
        return
    peers = message.get(b'peers')
    if type(peers) is list:
        for p in peers:
            if type(p) is not dict:
                raise ValueError
            if type(p.get(b'ip')) is not bytes:
                raise ValueError
            port = p.get(b'port')
            if type(port) is not int or p <= 0:
                raise ValueError
            if b'peer id' in p:
                id = p.get(b'peer id')
                if type(id) is not bytes or len(id) != 20:
                    raise ValueError
    elif type(peers) is not bytes or len(peers) % 6 != 0:
        raise ValueError
    interval = message.get(b'interval', 1)
    if type(interval) is not int or interval <= 0:
        raise ValueError
    minint = message.get(b'min interval', 1)
    if type(minint) is not int or minint <= 0:
        raise ValueError
    if type(message.get(b'tracker id', b'')) is not bytes:
        raise ValueError
    npeers = message.get(b'num peers', 0)
    if type(npeers) is not int or npeers < 0:
        raise ValueError
    dpeers = message.get(b'done peers', 0)
    if type(dpeers) is not int or dpeers < 0:
        raise ValueError
    last = message.get(b'last', 0)
    if type(last) is not int or last < 0:
        raise ValueError

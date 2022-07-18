from websocket import create_connection
from threading import Thread
from time import sleep


def wsrecvloop(ws, msglist):
    while True:
        nextline = ws.recv()
        msglist.append(nextline)


def test_server_connect(app_instance):
    app_instance.start()
    sleep(1)

    ws = create_connection('ws://127.0.0.1:5000/senduci')
    ws.send('uci')

    msglist = []
    p1 = Thread(target=wsrecvloop, args=(ws, msglist))
    p1.start()
    p1.join(timeout=2)

    # Ensure messages are received in the correct order
    # line 1 contains engine name
    assert 'stockfish' in msglist[0].lower()

    # lines 2 to 3 start with id
    for line in msglist[1:3]:
        assert line.startswith('id')

    # lines 5 to -2 start with option
    for line in msglist[5:-1]:
        assert line.startswith('option')

    # last line is uciok
    # lines 5 to -2 start with option
    assert msglist[-1] == 'uciok'

    # Disconnect client
    ws.close()

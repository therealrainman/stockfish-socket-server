from websocket import create_connection
from threading import Thread


def wsrecvloop(ws, msglist):
    while True:
        nextline = ws.recv()
        msglist.append(nextline)


def test_server_connect(app_instance):
    app_instance.start()

    ws = create_connection('ws://0.0.0.0:5000/senduci')
    ws.send('uci')

    msglist = []
    p1 = Thread(target=wsrecvloop, args=(ws, msglist))
    p1.start()
    p1.join(timeout=2)

    print('\n'.join(msglist))

    ws.close()
    print('about to shutdown!')

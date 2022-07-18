import pytest
from stockfish_socket_server.models import StockfishSocketEmitter


def test_invalid_stockfish_path():
    with pytest.raises(ValueError):
        StockfishSocketEmitter(stockfish_path='/fake/folder/fake/file')


def test_send_uci():
    emitter = StockfishSocketEmitter(stockfish_path='/usr/local/bin/stockfish')
    emitter._create_stockfish_process()

    # Check initial engine message
    assert 'stockfish' in emitter.stockfish_process.stdout\
                            .readline().lower().strip()

    # Check isready response
    emitter.send_uci('isready')
    assert emitter.stockfish_process.stdout\
            .readline().lower().strip() == 'readyok'

    emitter.stop()

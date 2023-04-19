# stockfish-socket-server
Simple WebSocket server for running Stockfish chess engine on a remote machine.

## Quickstart with Docker

Using the `docker-compose.yml` file:
```bash
$ docker compose up -d
```

Or running manually:
```bash
$ docker run \
    -d -p 5000:5000 \
    --entrypoint=/bin/bash \
    ghcr.io/x64squared/stockfish-socket-server \
    /stockfish-socket-server/start_server.sh
```

## Starting the server manually

1. Install requirements through `pip` (recommended with a virtual environment):
```bash
$ cd stockfish-socket-server
$ pip install -r requirements.txt
```

2. Start the server with `gunicorn` (recommended options from `start_server.sh`):
```bash
$ gunicorn \
    --bind 0.0.0.0:5000 \
    -w 4 \
    -t 8 \
    --timeout 0 \
    'run:create_app(stockfish_path="/usr/local/bin/stockfish")'
```

## Connecting to the server

[stockfish-socket-client](https://github.com/x64squared/stockfish-socket-client) can be used to connect to the server; an example of using the client in command line mode:

```
$ stockfish-socket-client
Stockfish 15 by the Stockfish developers (see AUTHORS file)
isready
readyok
position startpos moves e2e4 e7e5
go depth 5
info string NNUE evaluation using nn-6877cd24400e.nnue enabled
info depth 1 seldepth 1 multipv 1 score cp 41 nodes 32 nps 32000 tbhits 0 time 1 pv g1f3
info depth 2 seldepth 2 multipv 1 score cp 164 nodes 63 nps 63000 tbhits 0 time 1 pv g1f3 a7a6 f3e5
info depth 3 seldepth 3 multipv 1 score cp 148 nodes 139 nps 139000 tbhits 0 time 1 pv d1h5 a7a6 h5e5 g8e7
info depth 4 seldepth 4 multipv 1 score cp 148 nodes 214 nps 107000 tbhits 0 time 2 pv d1h5 a7a6 h5e5 g8e7
info depth 5 seldepth 5 multipv 1 score cp 75 nodes 1308 nps 436000 tbhits 0 time 3 pv g1f3 g8f6 d2d4 f6e4
bestmove g1f3 ponder g8f6
```

 The client runs exactly like a local instance of stockfish, and therefore integrates with any UCI-compatible chess GUI program. More usage information can be found in the [client README file](https://github.com/x64squared/stockfish-socket-client/blob/main/README.md).

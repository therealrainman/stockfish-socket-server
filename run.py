import argparse
from pathlib import Path
from stockfish_socket_server import app

def create_app(stockfish_path, debug_mode=False):
    app.config['DEBUG'] = debug_mode
    app.config['stockfish_path'] = stockfish_path

    return app

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--stockfish-path', type=Path, required=True)
    parser.add_argument('--debug-mode', type=bool, default=False)
    args = parser.parse_args()

    if not args.stockfish_path.exists():
        raise ValueError(f'Stockfish executable not found at: {args.stockfish_path}')

    create_app(args.stockfish_path, args.debug_mode).run()

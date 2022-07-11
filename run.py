import argparse
from pathlib import Path
from stockfish_socket_server import app

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--stockfish-path', type=Path, required=True)
    parser.add_argument('--debug-mode', type=bool, default=False)
    args = parser.parse_args()

    if not args.stockfish_path.exists():
        raise ValueError(f'Stockfish executable not found at: {args.stockfish_path}')

    app.config['stockfish_path'] = args.stockfish_path
    app.run(args.debug_mode)

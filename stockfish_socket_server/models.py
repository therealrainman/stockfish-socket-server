import subprocess
from pathlib import Path
from threading import Thread, Event


class StockfishSocketEmitter:
    """
    Emitter class to handle messages and send the engine output to the client.
    """
    def __init__(self, stockfish_path):
        if not Path(stockfish_path).exists():
            raise ValueError(f'No executable found at: {stockfish_path}')

        self.stockfish_path = stockfish_path
        self.stockfish_process = None
        self.emitter_thread = None
        self.stop_signal = Event()

    def _create_stockfish_process(self):
        """
        Create the stockfish process
        :return: None
        """
        if not self.stockfish_process:
            self.stockfish_process = subprocess.Popen(
                self.stockfish_path,
                universal_newlines=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

    def send_uci(self, command):
        """
        Send the uci command to the engine
        :param command: uci command
        :return: None
        """
        self.stockfish_process.stdin.write(f'{command}\n')
        self.stockfish_process.stdin.flush()

    def emit_stockfish_stdout(self, ws, stop_signal):
        """
        Send the engine stdout to the client; close client connection on quit command
        :param ws: Websocket connection
        :param stop_signal: Event to signal stop requested and close client connection
        :return: None
        """
        while not stop_signal.wait(0):
            if not self.stockfish_process.stdout:
                raise BrokenPipeError()
            if self.stockfish_process.poll() is not None:
                raise RuntimeError('No Stockfish process running')
            stockfish_stdout = self.stockfish_process.stdout.readline().strip()
            ws.send(stockfish_stdout)
        ws.send('Quit command received, exiting...')
        ws.close(message='quit_command_received')

    def start(self, ws):
        """
        Start the Websocket server
        :param ws: Websocket connection
        :return: None
        """
        self._create_stockfish_process()
        self.emitter_thread = Thread(
            target=self.emit_stockfish_stdout,
            args=(ws, self.stop_signal)
        )
        self.emitter_thread.setDaemon(True)
        self.emitter_thread.start()

    def stop(self):
        """
        Stop the Websocket server, and kill the stockfish process
        :return: None
        """
        if self.stockfish_process.poll() is None:
            self.stop_signal.set()
            self.send_uci('quit')
            self.stockfish_process.kill()
            while self.stockfish_process.poll() is None:
                pass

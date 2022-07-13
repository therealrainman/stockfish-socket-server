import subprocess
from threading import Thread, Event


class StockfishSocketEmitter:
    def __init__(self, stockfish_path):
        self.stockfish_path = stockfish_path
        self.stockfish_process = None
        self.emitter_thread = None
        self.stop_signal = Event()

    def send_uci(self, command):
        self.stockfish_process.stdin.write(f'{command}\n')
        self.stockfish_process.stdin.flush()

    def emit_stockfish_stdout(self, ws, stop_signal):
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
        if not self.stockfish_process:
            self.stockfish_process = subprocess.Popen(
                self.stockfish_path,
                universal_newlines=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

        self.emitter_thread = Thread(
            target=self.emit_stockfish_stdout,
            args=(ws, self.stop_signal)
        )
        self.emitter_thread.setDaemon(True)
        self.emitter_thread.start()

    def stop(self):
        if self.stockfish_process.poll() is None:
            self.stop_signal.set()
            self.send_uci('quit')
            self.stockfish_process.kill()
            while self.stockfish_process.poll() is None:
                pass

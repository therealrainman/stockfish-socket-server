import pytest
from threading import Thread
from run import create_app


@pytest.fixture
def app_instance():
    app = create_app('/usr/local/bin/stockfish')
    app_instance_thread = Thread(target=app.run)
    app_instance_thread.daemon = True
    return app_instance_thread

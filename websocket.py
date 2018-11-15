import tornado.websocket
import tornado.ioloop
from tornado import gen
import signal
import json
import base64
from test_websocket import update_data

HOST="localhost"
PORT = 8888
ENDPOINT="ws"

class Client():
    def __init__(self, url, **kwargs):
        self.url = url
        self.ws = None
        self.io_loop = tornado.ioloop.IOLoop.current()
        self.periodiccallback_func = kwargs.get("periodiccallback_func", None)
        self.callback_time = kwargs.get("callback_time", None)
        self
        
    
    @gen.coroutine
    def connect(self):
        try:
            self.ws = yield tornado.websocket.websocket_connect(self.url)
        except Exception:
            print(f"Failed to connect to websocket at {self.url}")
        else:
            print(f"Successfully connected to websocket at {self.url}")
            self.ws.write_message(json.dumps({"newClient": "device"}), binary=False)
            while True:
                msg = yield self.ws.read_message()
                if msg is None:
                    break
                else:
                    print(f"Incoming message: {msg}")

    def send_data(self, data):
        out = {
            "id": "device",
            "img": data
        }
        self.ws.write_message(json.dumps(out), binary=False)

    def run(self):
        self.connect()
        tornado.ioloop.PeriodicCallback(
            self.periodiccallback_func,
            self.callback_time
        ).start()
        self.io_loop.start()

    def shutdown(self, signum, frame):
        self.ws.close()
        self.io_loop.add_callback_from_signal(self.io_loop.stop)

def main():
    url = f"ws://{HOST}:{PORT}/{ENDPOINT}"
    client = Client(url, callback_time=2000)
    client.periodiccallback_func = lambda: update_data(client)
    signal.signal(signal.SIGINT, client.shutdown)
    client.run()
    
if __name__ == '__main__':
    main()
    
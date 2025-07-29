# scripts/gesture.py

import socket
import threading

class GestureListener:
    def __init__(self, port):
        self._cmd = None
        self._port = port
        threading.Thread(target=self._listen, daemon=True).start()

    def _listen(self):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("localhost", self._port))
            while True:
                data = client.recv(1024)
                if not data:
                    break
                self._cmd = data.decode()
        except Exception as e:
            print(f"Gesture listener error on port {self._port}: {e}")

    def pop(self):
        cmd, self._cmd = self._cmd, None
        return cmd

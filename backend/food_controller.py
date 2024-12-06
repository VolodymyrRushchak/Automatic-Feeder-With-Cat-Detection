import socket
import struct


class FoodController:
    def __init__(self, s: socket):
        self.connection = s.makefile('wb')
        self.feeding = False

    def start_feeding(self) -> None:
        self.connection.write(struct.pack('<c', b'1'))
        self.connection.flush()
        self.feeding = True

    def stop_feeding(self) -> None:
        self.connection.write(struct.pack('<c', b'0'))
        self.connection.flush()
        self.feeding = False

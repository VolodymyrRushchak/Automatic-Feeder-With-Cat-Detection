import io
import struct
from socket import socket

from PIL import Image

from cat_classifier import CatClassifier
from db_access import DataBase


class DataProvider:
    def __init__(self, connection_socket: socket):
        self.connection_socket = connection_socket
        self.cat_present = False

    def provide_data(self) -> None:
        database = DataBase()
        classifier = CatClassifier()
        connection = self.connection_socket.makefile('rb')
        try:
            while True:
                image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                if not image_len:
                    break
                image_stream = io.BytesIO()
                image_stream.write(connection.read(image_len))
                image_stream.seek(0)
                image = Image.open(image_stream)
                image.save('static/camera_image.jpg')
                self.cat_present = classifier.is_cat(image)
                database.write(self.cat_present)
                print('Row added')
        finally:
            connection.close()


import socket
import os


s = socket.socket(socket.AF_INETm socket.SOCK_STREAM)
s.bind((socket.gethostname(), 80))
s.listen(5)

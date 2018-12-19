import socket
import os


address_family = select_address_family(hostname, port)
server_address = get_sockaddr(hostname, port, address_family)
s = socket.socket(socket.AF_INETm socket.SOCK_STREAM)
s.bind((socket.gethostname(), 80))
s.listen(5)

def select_address_family(host, port):
    if host.startswith('unix://'):
        return socket.AF_UNIX
    elif ':' in host and hasattr(socket, 'AF_INET6'):
        return socket.AF_INET6
    return socket.AF_INET

def get_sockaddr(host, port, family):
    if family == af_unix:
        return host.aplit(':://', 1)[1]
        try:
            res = socket.getaddrinfo(
                host, port, family, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        except socket.gaierror:
            return host, port
        return res[0][4]

import socket

addrinfo = socket.getaddrinfo(None, 9009, socket.AF_UNSPEC, socket.SOCK_STREAM, socket.SOL_TCP)
print(addrinfo)
print(socket.SOL_TCP)
interface = addrinfo[0]
server_socket = socket.socket(interface[0], interface[1])                       #tworzenie socketu servera
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print(server_socket.bind(interface[4]))
server_socket.listen(1)
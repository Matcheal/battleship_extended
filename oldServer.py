# Echo server program
import socket
import datetime
import string
import array

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 1025  # Arbitrary non-privileged port
RECV_BUFFER = 4096
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)

    while True:
        conn, addr = s.accept()
        print('Client', addr, 'connected.')
        message = ""
        while message != "end()":
            data = conn.recv(RECV_BUFFER)
            print("[Client] " + data.decode("utf-8"))
            message = input()
            conn.send(bytearray(message, encoding="utf8"))
        conn.close()

except socket.error as e:
    print("Socket error({0}): {1}".format(e.errno, e.strerror))

except KeyboardInterrupt:
    print("Closing server")
    conn.close()

except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
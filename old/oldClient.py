# Echo client program
import socket
import sys
RECV_BUFFER = 4096
argc = len(sys.argv)

if argc > 2:
    #HOST = 'localhost'    # The remote host
    HOST = sys.argv[2]
else:
    HOST = '127.0.0.1'    # The remote host

if argc >1:
    PORT = int(sys.argv[1])              # The same port as used by the server
else:
    PORT = 1025              # The same port as used by the server

for c in range( argc):
    print( "Arg" + str(c) + "=" + sys.argv[c] )

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(b'Hello, world')
    message = ""
    while message != "end()":
        data = s.recv(RECV_BUFFER)
        print('[Server] ', data.decode("utf-8"))
        message = input()
        s.send(bytearray(message, encoding="utf8"))

    s.close()

except socket.error as e:
    print ("Socket error({0}): {1}".format(e.errno, e.strerror))
except:
    print ("Unexpected error:", sys.exc_info()[0])
    raise
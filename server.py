import sys
import socket
import select

HOST = ''
RECV_BUFFER = 4096
PORT = 9009

def chat_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)

        # add server socket object to the list of readable connections
        # SOCKET_LIST.append(server_socket)

        print("Battleship server started on port  " + str(PORT))
        client_socket, addr = server_socket.accept()
        print("Client " + str(addr) + " connected")
        socket_list = [sys.stdin, client_socket]

        while True:

            # get the list sockets which are ready to be read through select
            # 4th arg, time_out  = 0 : poll and never block

            ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [], 0)

            for sock in ready_to_read:
                if sock == client_socket:
                    # incoming message from remote server, s
                    data = sock.recv(4096)
                    if not data:
                        print('\nDisconnected from server')
                        sys.exit()
                    else:
                        # print data
                        sys.stdout.write(data.decode("utf-8"))
                        sys.stdout.write('[Me] ')
                        sys.stdout.flush()

                else:
                    # user entered a message
                    msg = sys.stdin.readline()
                    client_socket.send(("\r[Server] " + msg).encode("utf-8"))
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()

        server_socket.close()

    except socket.error as e:
        print("Socket error({0}): {1}".format(e.errno, e.strerror))

    except KeyboardInterrupt:
        print("Closing server")
        client_socket.close()

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

if __name__ == "__main__":
    sys.exit(chat_server())
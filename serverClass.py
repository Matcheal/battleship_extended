import sys
import socket
import select
import battleshipBoard

HOST = ''
RECV_BUFFER = 4096
PORT = 9009

class Server:

    def __init__(self):
        self.main()

    def main(self):
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

            clientBoard = battleshipBoard.Board()
            localBoard = battleshipBoard.Board()
            localBoard.initShips("ready")

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
                        else:       #ODCZYT__ODCZYT__ODCZYT__ODCZYT__ODCZYT__ODCZYT__ODCZYT
                            # print data
                            readableData = data.decode("utf-8")[0:-1]
                            sys.stdout.write("\r[Client] ")
                            sys.stdout.write(data.decode("utf-8"))
                            sys.stdout.flush()

                            # if readableData == "Hit!"
                            #
                            # if localBoard.ifHit(readableData):
                            #     client_socket.send(("Hit!\n").encode("utf-8"))
                            #     sys.stdout.write('[Me] ')
                            #     sys.stdout.flush()
                            # else:
                            #     client_socket.send(("Missed!\n").encode("utf-8"))
                            #     sys.stdout.write('[Me] ')
                            #     sys.stdout.flush()

                            sys.stdout.write('[Me] ')
                            sys.stdout.flush()

                    else:           #ZAPIS__ZAPIS__ZAPIS__ZAPIS__ZAPIS__ZAPIS__ZAPIS__ZAPIS
                        # user entered a message
                        msg = sys.stdin.readline()
                        if str(msg) == "print\n":
                            localBoard.print()
                            sys.stdout.write('[Me] ')
                            sys.stdout.flush()
                        elif str(msg) == "oponent\n":
                            clientBoard.print()
                            sys.stdout.write('[Me] ')
                            sys.stdout.flush()
                        else:
                            client_socket.send(msg.encode("utf-8"))
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

instance = Server()

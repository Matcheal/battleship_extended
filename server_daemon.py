import sys
import socket
import battleshipBoard
import random
from daemon import Daemon
import syslog
import time

RECV_BUFFER = 4096


class Server(Daemon):
    def __init__(self, pidfile):
        super(Server, self).__init__(pidfile)
        port = int(sys.argv[2]) if len(sys.argv) == 3 else 9009
        # port = 9009
        try:

            try:
                serverInfo = socket.getaddrinfo(None, port, socket.AF_UNSPEC, socket.SOCK_STREAM, socket.SOL_TCP)
            except Exception as e:
                print("getaddrinfo error: ", e)
                sys.exit()
            self.server_socket = None
            for interface in reversed(serverInfo):
                try:
                    self.server_socket = socket.socket(interface[0], interface[1])                           #tworzenie socketu servera
                    self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.server_socket.bind(interface[4])
                    self.server_socket.listen(1)
                    print(interface[0], interface[4])
                    break
                except:
                    self.server_socket.close()
                    continue
            if not self.server_socket:
                print("Could not create server socket, exiting.")
                sys.exit()
            print("Battleship server started on port  " + str(port))
            self.lastGuessStack = list()  # stos przechowujący ostatnie zgadywane położenie
            self.guessStack = list()
            self.oponentBoard = battleshipBoard.Board()  # inicjalizacja planszy przeciwnika
            self.localBoard = battleshipBoard.Board()  # inicjalizacja planszy gracza


        except socket.error as e:
            print("Socket error({0}): {1}".format(e.errno, e.strerror))

        except KeyboardInterrupt:
            print("Closing server")
            self.client_socket.close()

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise



     # DAEMON START
    def run(self):
        syslog.openlog("Battleship server bot", syslog.LOG_PID, syslog.LOG_LOCAL7)

        self.client_socket, addr = self.server_socket.accept()                                       # akceptowanie połączenia z klientem
        syslog.syslog(syslog.LOG_INFO, "Client " + str(addr) + " connected")
        self.localBoard.initShips("random")                                                           #wpisanie położenia statków gracza
        self.client_socket.send(("Opponent ready!\n").encode("utf-8"))                               #wyślij wiadomość gotowości do przeciwnika
        self.localBoard.syslogBoardState()
        syslog.syslog(syslog.LOG_INFO, "Wait for your opponent to initiate their's ships.")

        while True:
            # incoming message from remote server, s
            data = self.client_socket.recv(RECV_BUFFER)
            if not data:
                syslog.syslog(syslog.LOG_INFO, '\nDisconnected from server')
                sys.exit()
            else:                                                                                    # ODCZYT, obsługa odczytu wiadomości
                # print data
                readableData = data.decode("utf-8")[0:-1]
                syslog.syslog(syslog.LOG_INFO, "[Opponent]" + data.decode("utf-8"))

                if readableData == "Hit!":
                    self.oponentBoard.insertByCoor(self.lastGuessStack.pop(), battleshipBoard.HIT_SYMBOL)
                elif readableData == "Missed!":
                    self.oponentBoard.insertByCoor(self.lastGuessStack.pop(), battleshipBoard.MISSED_SYMBOL)
                elif readableData == "Game over.":
                    syslog.syslog(syslog.LOG_INFO, "You WON!")
                    exit()
                elif readableData == "Opponent ready!":
                    continue

                else:
                    if self.localBoard.ifHit(readableData):
                        self.client_socket.send(("Hit!\n").encode("utf-8"))
                        if self.localBoard.countSymbols(battleshipBoard.SHIP_SYMBOL) == 0:
                            syslog.syslog(syslog.LOG_INFO, "End of game, You LOST!")
                            self.client_socket.send(("Game over.\n").encode("utf-8"))

                    else:
                        self.client_socket.send(("Missed!\n").encode("utf-8"))
                    syslog.syslog(syslog.LOG_INFO, "-->Your turn!")
                    self.localBoard.yourTurn = True
                    time.sleep(2)
                    syslog.syslog(syslog.LOG_INFO, self.respond())

        self.server_socket.close()

    def respond(self):
        while True:
            xPosition = random.randint(1, 10)
            yPosition = random.randint(1, 10)
            coor = str(list(battleshipBoard.Board.dictionary.keys())[list(battleshipBoard.Board.dictionary.values()).index(yPosition)]) + str(xPosition) + "\n"
            if self.oponentBoard.validCoor(coor.rstrip()) and coor not in self.guessStack:
                break

        if self.localBoard.yourTurn:
            self.client_socket.send(coor.encode("utf-8"))
            self.lastGuessStack.append(coor)  # w celu ustalenia kolejnosci
            self.guessStack.append((coor))
            self.localBoard.yourTurn = False
        return coor

if __name__ == "__main__":
        daemon = Server('/tmp/server-daemon.pid')
        if len(sys.argv) == 3 or len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print("Unknown command")
                        sys.exit(2)
                sys.exit(0)
        else:
                print("usage: %s start|stop|restart  port" % sys.argv[0])
                sys.exit(2)

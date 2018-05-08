import sys
import socket
import select


def chat_client():
    host = sys.argv[2] if len(sys.argv) > 2 else '127.0.0.1'
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9009
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print('Unable to connect')
        sys.exit()
    print('Connected to remote host. You can start sending messages')
    sys.stdout.write('[Me] ')
    sys.stdout.flush()

    while True:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

        for sock in ready_to_read:
            if sock == s:
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
                s.send(("\r[Client] " + msg).encode("utf-8"))
                sys.stdout.write('[Me] ')
                sys.stdout.flush()


if __name__ == "__main__":
    sys.exit(chat_client())
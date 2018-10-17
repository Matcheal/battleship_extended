# Description :page_facing_up:
Project [**battleship**](https://github.com/Matcheal/battleship) extended by:
* server running as a daemon,
* implementation of syslog for the server and "bot" mode for the server (computer opponent),
* DNS service realized with getaddrinfo()
# Usage
* Run the server `python3 server_daemonpy`. Additionally, port can be specified while executing the server i.e. `python3 server_daemonpy 1025`. Server acts as another player (bot) and runs in the background. Its terminal output is forwarded to log `var/log/local7`. 
* Run client.py with specified _port_ and _host name_ e.g. `python3 client.py 1025 localhost`. *Port* defaults to _9009_ and *host* to _127.0.0.1_ (localhost).
* When the client has successfully connected to the server, a proper message is displayed and the game has started.
* Player starts the game by sending first coordinates in the proper format. Coordinates should consist of a letter for a vertical axis and a number for horizontal axis, range **A - J** and **1 - 10**. The order (_letter, number_) should be of no significance.
* To check player board, type `player` into terminal. To check our current knowledge about the opponent board, type `opponent` and press enter.
* To instantly finish the game, press ^C.

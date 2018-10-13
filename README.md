# Description :page_facing_up:
Project [**battleship**]() extended by:
* server running as a daemon,
* implementation of syslog for the server and "bot" mode for the server (computer opponent),
* DNS service realized with getaddrinfo(https://github.com/Matcheal/battleship)
# Usage
* Run the server `python3 server_daemonpy`. Additionally, port can be specified while executing the server i.e. `python3 server_daemonpy 1025`. Server acts as another player (bot) and runs in the background. Its terminal output is forwarded to log `var/log/local7`. 
* Run client.py with specified _port_ and _host name_ e.g. `python3 client.py 1025 localhost`. *Port* defaults to _9009_ and *host* to _127.0.0.1_ (localhost).
* To instantly finish the game, press ^C.

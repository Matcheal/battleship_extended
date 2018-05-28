import sys
import os
import time
import atexit
import signal


class Daemon:
    """Usage: subclass the daemon class and override the run() method."""

    def __init__(self, pidfile):
        self.pidfile = pidfile                                          #podana sciezka do utworzenia pliku pidfile

    def daemonize(self):                                                #metoda do inicjalizacji demona
        """Deamonize class. UNIX double fork mechanism."""

        try:
            pid = os.fork()                                             #pierwszy fork, proces potonmy działa w tle,
            if pid > 0:                                                 #proces dziedziczy identyfikator grupy ale otrzymuje swój własny PID
                # exit first parent                                     #pewnosc, ze proces nie jest przywodca grupy procesow
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)

        # decouple from parent environment
        os.chdir('/')                                                   #zmiana katalogu roboczego

        os.setsid()                                                     #utworzenie nowej sesji, proces staje sie przywodca nowej grupy procesow, bez terminala sterujacego

        os.umask(0)                                                     #zerowanie maski trybu dostepu do tworzonych plikow

        signal.signal(signal.SIGHUP, signal.SIG_IGN)                    #ignorujemy sygnal SIGHUP, poniewaz jest on wysylany do potomkow po zamknieciu przywodcy sesji
        # do second fork
        try:
            pid = os.fork()                                             #zamykamy proces macierzysty; zapobiegamy automatycznegou uzyskaniu terminala sterujacego przez nasz proces
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        os.setuid(1000)                                                  #zmiana właściciela procesu

        # write pidfile
        atexit.register(self.delpid)

        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f:
            f.write(pid + '\n')

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """Start the daemon."""

        # Check for a pidfile to see if the daemon already runs
        try:
            with open(self.pidfile, 'r') as pf:

                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            message = "pidfile {0} already exist. " + \
                      "Daemon already running?\n"
            sys.stderr.write(message.format(self.pidfile))
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """Stop the daemon."""

        # Get the pid from the pidfile
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = "pidfile {0} does not exist. " + \
                      "Daemon not running?\n"
            sys.stderr.write(message.format(self.pidfile))
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err.args))
                sys.exit(1)

    def restart(self):
        """Restart the daemon."""
        self.stop()
        self.start()

    def run(self):
        """You should override this method when you subclass Daemon.

        It will be called after the process has been daemonized by
        start() or restart()."""
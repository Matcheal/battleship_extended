import battleshipBoard
import syslog
import os
board = battleshipBoard.Board()

# syslog.setlogmask(syslog.LOG_UPTO(syslog.LOG_NOTICE))
# syslog.openlog("loggingTEST", syslog.LOG_PID, syslog.LOG_LOCAL7)
# syslog.syslog('kawa')
# board.syslogBoardState()
# syslog.closelog()
#
print(os.sysconf("SC_OPEN_MAX"))




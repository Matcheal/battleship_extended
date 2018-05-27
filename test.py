import battleshipBoard
import syslog
board = battleshipBoard.Board()

# syslog.setlogmask(syslog.LOG_UPTO(syslog.LOG_NOTICE))
# syslog.openlog("loggingTEST", syslog.LOG_PID, syslog.LOG_LOCAL7)
# syslog.syslog('kawa')
# board.syslogBoardState()
# syslog.closelog()

print(battleshipBoard.Board.reverseDict(2))
lista = [1,2,3,4]
strCoor = "{}{} {}{}".format(1, 2, 3, 4)
print(strCoor)




'''
    Name: Linux automated regression testing of desktop
    Function: Check iso changges and start test
    Author: peng.li@i-soft.com.cn
    Time: 20161008
'''
import os
from control import *
from logging_config import *
from subprocess import check_output

Logging_Config.setlogger('Lart_i_desktop', 'Lart_i_desktop.log')
lartlogger = logging.getLogger('Lart_i_desktop')

def getxmlpath():
    homedir = check_output("pwd").strip('\n')
    xmlpath = os.path.join(homedir, 'setup.xml')
    print xmlpath
    return xmlpath

if __name__ == "__main__":
    setupxml = getxmlpath()
    lartdesktop = Main(setupxml)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            lartlogger.info('lart_i desktop start')
            lartdesktop.start()
        elif 'stop' == sys.argv[1]:
            lartlogger.info('lart_i desktop stop')
            lartdesktop.stop()
        elif 'restart' == sys.argv[1]:
            lartlogger.info('lart_i desktop restart')
            lartdesktop.restart()
        else:
            lartlogger.error("unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("useage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)


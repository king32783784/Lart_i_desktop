import sys
import time
import multiprocessing
import linecache
import logging
from initdaemon import Daemon
from checkiso import CheckUpdate
from starttest import DoTest

lartlogger = logging.getLogger('desktoplogger')

class IsoCheck(multiprocessing.Process, CheckUpdate):
    '''
        Check whether there is a need to test iso
    '''
    def __init__(self, setupxml):
        multiprocessing.Process.__init__(self)
        self.setupxml = setupxml
    
    def run(self):
        while True:
            isocheck = CheckUpdate()
            isocheck.getisolist(self.setupxml)
            lartlogger.info("check one time")
            time.sleep(10)

class TestControl(multiprocessing.Process, DoTest):
    '''
        Control iso install and start iso test.
    '''
    def __init__(self, setupxml, installtool):
        multiprocessing.Process.__init__(self)
        self.xml = setupxml
        self.tool = installtool

    def run(self):
        self.isoinstall(self.xml, self.tool)

class Main(Daemon):
    
    def __init__(self, setupxml):
        Daemon.__init__(self)
        self.setupxml = setupxml
 
    
    def _run(self):
       controlist = []
       control = IsoCheck(self.setupxml)
       controlist.append(control)
       control.start()
       lartlogger.info(control.pid)
       file('/tmp/daemon.pid', 'a+').write("%s\n" % control.pid)
       for control in controlist:
           control.join()

a = TestControl('/home/Lart_i_desktop/setup.xml', '/home/Lart_i_desktop/autoinstall.sh')
a.run()

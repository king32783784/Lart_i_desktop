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
    
    def __init__(self, setupxml, testtool):
        Daemon.__init__(self)
        self.setupxml = setupxml
        self.tool = testtool
 
    
    def _run(self):
        threadlist = []
        isocheck = IsoCheck(self.setupxml)
        threadlist.append(isocheck)
        isocheck.start()
        lartlogger.info(isocheck.pid)
        file('/tmp/daemon.pid', 'a+').write("%s\n" % isocheck.pid)
        testcontrol = TestControl(self.setupxml, self.tool)
        threadlist.append(testcontrol)
        testcontrol.start()
        lartlogger.info(testcontrol.pid)
        fiel('/tmp/daemon.pid', 'a+').write("%s\n" % testcontrol.pid)
        for control in controlist:
            control.join()

a = TestControl('/home/Lart_i_desktop/setup.xml', '/home/Lart_i_desktop/autoinstall.sh')
a.run()

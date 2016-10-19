import os
import re
import urllib
import urllib2
import logging
import shutil
from subprocess import PIPE, Popen, call
from prepare import getsetupinfo

lartlogger = logging.getLogger('desktoplogger')

def downloadfile(local_dir, url):
    try:
        response = urllib2.urlopen(url)
        urllib.urlretrieve(url, local_dir)
    except:
        lartlogger.error('\tError download the file:', local_dir)
        exit(1)


class DoTest(object):
     
    def parsingisolist(self, setupinfo):
        isolist = os.path.join(setupinfo['xml_dict']['testtooldir'][0], 
                               "testisolist")
        f = open(isolist, 'r')
        firstline = f.readline()
        isoname = re.findall(r"(.+)&&&&", firstline)   
        isoname = isoname[0] + ".iso"
        isolink = re.findall(r"&&&&(.+)", firstline)
        isolink = isolink[0] + '/' + isoname
        isoitem = [isoname, isolink]
        return isoitem

    def downloadiso(self, isoitem, setupinfo):
        locatedir = os.path.join(setupinfo['xml_dict']['testtooldir'][0],
                                 isoitem[0])
        downloadfile(locatedir, isoitem[1])
        sumurl=isoitem[1] + '.sha256'
        shafile = urllib2.urlopen(sumurl).read()
        isosha = Popen('sha256sum %s' %locatedir, stdout=PIPE, shell=True)
        isoshavalue = isosha.communicate()[0]
        if isoshavalue[0:65] == shafile[0:65]:
            return "ready"
        else:
            return "unready"
 
    def setautostarttest(self):
        shutil.copyfile('/home/test/Lart_i_desktop/test_iso.sh', '/tmp/inst/rootdir/home/test/test_iso.sh')
        f = open('/tmp/inst/rootdir/etc/profile', 'a+')
        f.write('/bin/sh /home/test/test_iso.sh &')
        call('reboot', shell=True)
    
    def isoinstall(self, xml, installtool):
        setupinfo = getsetupinfo(xml)
        isoitem = self.parsingisolist(setupinfo)
        isostatus = self.downloadiso(isoitem, setupinfo)
        testiso = os.path.join(setupinfo['xml_dict']['testtooldir'][0],
                               isoitem[0])
        installpart = setupinfo['xml_dict']['testpart'][0]
        if isostatus == "ready":
            installcmd = "sh " + installtool + " " + installpart + " " + testiso
            install = Popen(installcmd, stdout=PIPE, shell=True)
            installstatus = install.communicate()[0]
            lartlogger.info(installstatus)
        else:
            lartlogger.error("Test iso check failed")
            exit(1)
        self.setautostarttest()
        
        
#a=PrepareIso('/home/Lart_i_desktop/setup.xml', '/home/Lart_i_desktop/autoinstall.sh')
#b=a.isoinstall()   

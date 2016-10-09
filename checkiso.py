import urllib2
import re
import os
import logging
from subprocess import Popen, PIPE
from prepare import getsetupinfo

lartlogger = logging.getLogger('Lart_i_desktop')

def downloadfile(local_dir, url):
    try:
        response = urllib2.urlopen(url)
        urllib.urlretrieve(url, local_dir)
    except:
        print '\tError download the file:', local_dir
        exit(1)

class CheckUpdate(object):

    def get_htmlcontent(self, xmlurl, remode):
        try:
            html_Context = urllib2.urlopen(xmlurl).read()
        except urllib2.HTTPError:
            lartlogger.error('%s is open failed' % xmlurl) # need report this error
        html_Context = unicode(html_Context, 'utf-8')
        return re.findall(r"%s" % remode, html_Context)

    def getisolist(self, setupxml):
        setupinfo = getsetupinfo(setupxml)
        xmlurl = setupinfo['xml_dict']['isourl'][0]
       #  remode = "href=\"(.+).iso\">" # iso url
        remode = "href=\"(.+?)/\">[r/b/R/B]" # http://koji.isoft.zhcn.cc/iso/isoft4.0/
        isopathlist = self.get_htmlcontent(xmlurl, remode)
        isolist = []
        linklist = []
        for k, isotype in enumerate(isopathlist):
            remode = "href=\"(.+).iso\">"
            link = xmlurl + isotype
            isoname = self.get_htmlcontent(link, remode)
            isolist.append(isoname)
            linklist.append(link)
        print linklist
        testiso = isolist[-1][0]
        testlink = linklist[-1]
        testitem = testiso + "&&&&" + testlink
        f = open('testisolist', 'a+')
        Type="Y"
        for line in f.xreadlines():
            if line.strip('\n') == testiso:
                Type="N"
                break
        if Type == "Y":
            f.write('%s\n' % testitem)

    def getisomd5(self, testiso):
        xmlurl = os.path.join(self.setup['xml_dict']['isourl'][0],
                              testiso) + '.md5sum'
        remode = "(.+)"
        lartlogger.info(xmlurl)
        targetmd5 = self.get_htmlcontent(xmlurl, remode)
        return targetmd5[0]

    def downloadiso(self, testiso):
        locatedir = os.path.join(self.setup['xml_dict']['isoserver'][0],
                                 testiso)
        isourl = os.path.join(self.setup['xml_dict']['isourl'][0],
                              testiso)
        downloadfile(locatedir, isourl)
        filemdsum = Popen('md5sum %s' % locatedir, stdout=PIPE, shell=True)
        filemd5=filemdsum.communicate()[0]
        md5standard = self.getisomd5(testiso)
        if filemd5[0:32] == md5standard[0:32]:
            return "yes"
        else:
            return "no"

test = CheckUpdate()
test.getisolist('/home/desktop-iso/setup.xml')

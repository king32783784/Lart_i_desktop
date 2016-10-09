import os
import sys
import xml.dom.minidom
import linecache
import time
import logging

lartlogger = logging.getLogger('Lart_i_desktop')


class ParsingXml(object):
    '''
        Parsing xml files
    '''
    def __init__(self, xmlfilename, tagname='labelname'):
        self.xmlfile = xmlfilename
        self.tagname = tagname

    def parsing_label_list(self, labelname):
        '''
            Parsing Gets the list labels
        '''
        try:
            xmldom = xml.dom.minidom.parse(self.xmlfile)
            xmllabel = xmldom.getElementsByTagName(labelname)
        except IOError:
            lartlogger.error('Faile to open %s file, Please check it '
                             % self.xmlfile)
            exit(1)
        xmllabellist = []
        for singlelabel in xmllabel:
            xmllabellist.append(singlelabel.firstChild.data)
        return xmllabellist

    def specific_elements(self):
        '''
            Read the specific elements,call the class may need to override
            this function.By default returns a "xml_list" and "xml_dict" a
            dictionary of xml_list specify a label for the list xml_dict
            key for the XML element, the corresponding value for a list of
            corresponding element tag content
        '''
        xmllabels = self.parsing_label_list(self.tagname)
        xml_elements_dict = {}
        for perlabel in xmllabels:
            perxmllabellist = self.parsing_label_list(perlabel)
            xml_elements_dict[perlabel] = perxmllabellist
        xml_dict = { 'xml_list': xmllabels, 'xml_dict': xml_elements_dict}
        return xml_dict

def os_name():
    f = open('/etc/os-release', 'r')
    theline = linecache.getline("/etc/os-release", 5)
    osname_line = theline[13:-2]
    osname = osname_line.replace(' ', '_')
    return osname

def getsetupinfo(setupxml):
    '''
    'xml_list': [u'isourl', u'checkfrequency', u'testtooldir',
    u'isoserver', u'resultdir', u'comparingos', u'maillist']
    'xml_dict': {u'resultdir': [u'default'], u'isourl':
    [u'http://192.168.30.170/iso-images/'], u'testtmp': 
    [u'/var/cache'], u'checkfrequency': [u'60'], u'comparingos':
    [u'default'], u'maillist': [u'peng.li@i-soft.com.cn']}}
        '''
    test_setup = ParsingXml(setupxml, 'configlist')
    setupinfo = test_setup.specific_elements()
    lartlogger.info(setupinfo)
    return setupinfo

# testcase
# a=getsetupinfo()
# print(a)
# b=os_name()
# print(b)

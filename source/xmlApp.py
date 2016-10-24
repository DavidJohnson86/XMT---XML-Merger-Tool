'''
==============================================================================
Main modules for parsing and modifying Xml Files for BMW ACSM5 Project
==============================================================================
                            OBJECT SPECIFICATION
==============================================================================
$ProjectName: BMW ACSM5
$Source: xmlApp.py
$Revision: 1.1 $
$Author: David Szurovecz $
$Date: 2016/10/24 16:05:32CEST $
============================================================================
'''
import xml.etree.ElementTree as ET


class bmwXmlApp():

    def __init__(self, tree, root):
        self.tree = tree
        self.root = root

    def get_testnames(self):
        '''
        :return: list of names of the  Testcases
        '''
        arr = []
        for elem in self.root:
            values = elem.findall('ATTR')
            arr.append(values[7].attrib['val'])
        return arr

    def get_failedtest(self):
        '''
        :return: list of names of the Failed Testcases
        '''
        arr = []
        for elem in self.root:
            values = elem.findall('ATTR')
            if int(values[13].attrib['val']) > 0:
                arr.append(values[7].attrib['val'])
        return arr

    def get_testcasebydtc(self):
        '''
        :return: the name of the testcase what affected by a special dtc
        '''
        counter = 0
        for elem in self.root.findall('SEQ'):
            testname = elem[7].attrib['val']
            for sub in elem.findall('MEASV'):
                if sub.attrib['id'] == 'QUAL_DEQUAL.Lamps':
                    if sub.attrib['val1'] == 'B5,61,1CA' or sub.attrib['val1'] == '61,1CA,B5':
                        counter += 1
                        print testname
        print counter

    def get_isitrepaired(self, listofFailed):
        '''
        Takes the list of Failed Testcases. Iterating through the Number 2 Xml
        and if in Number 2 is passed what is failed in Number 1 Return a list
        with the names of the repairable testcases.
        :listofFailed: list of Failed Testcases
        :return: list of Passed Testcases what is failed before
        '''
        arr = []
        for elem in self.root:
            values = elem.findall('ATTR')
            if values[7].attrib['val'] in listofFailed and values[13].attrib['val'] == '0':
                arr.append(values[7].attrib['val'])

        return arr

    def get_rightValues(self, listofRepaired, destination_root, source_root, output):
        '''
        Get the right values,datas from the passed test cases
        :param list listofRepaired contains the passed testcases
        :param object pathroot is referring of the parsed passed testcases
        :return list with right values
        '''
        counter = 0
        fixed_test = []
        for elemone in destination_root.findall('SEQ'):
            testnameone = elemone[7].attrib['val']
            if testnameone in listofRepaired:
                # Found a Repairable testcase in the Retest Report
                # Now Find this in the Main report
                for elemtwo in source_root.findall('SEQ'):
                    testnametwo = elemtwo[7].attrib['val']
                    if testnameone == testnametwo:
                        fixed_test.append(testnameone)
                        # Found the same test in the Main Report
                        # check if the structure is the same
                        #source_root.insert(0, elemone)
                        source_root.remove(elemtwo)
                        destination_root.remove(elemone)
                        source_root.append(elemone)
                        destination_root.append(elemtwo)
                        #elemone.set(elemone.attrib['TestVariationIndex'], elemtwo)
                        counter += 1
        self.tree.write(str(output) + '\\output.xml', xml_declaration=True)
        return counter, fixed_test


'''--------------------------------------Init Input Datas-------------------------------------------------------------------------------------'''
if __name__ == "__main__":

    source = ET.parse(
        "d:\\10 ----------------Development----------------\\Python\\Xml_Parser\\Test_Files\Main Report\\ISC_Sensor_Emulation_Unknown_XmlReport.xml")
    source_root = source.getroot()
    destination = ET.parse(
        "d:\\10 ----------------Development----------------\\Python\\Xml_Parser\\Test_Files\Retested Report\\ISC_Sensor_Emulation_Unknown_XmlReport.xml")
    destination_root = destination.getroot()

    XmlobjFailed = bmwXmlApp(source, source_root)
    XmlobjPassed = bmwXmlApp(destination, destination_root)

    ''' Failed testcases'''
    #===============================================================================
    # listofFailed = XmlobjFailed.get_failedtest()
    # print 'These are the failed testcases: ', len(listofFailed), listofFailed
    #===============================================================================

    '''Number of Duplicated Testcases(if have)'''
    #===============================================================================
    #listofTestcases = list(XmlobjFailed.get_testnames())
    #difference = [i for i in set(listofTestcases)]
    # print 'The number of duplicated testcases: ', len(listofTestcases) - len(difference)
    #===============================================================================

    '''Check for repaired Testcases'''
    #===============================================================================
    # listofFailed = XmlobjFailed.get_failedtest()
    # repairedTests = XmlobjPassed.get_isitrepaired(listofFailed)
    # print 'These testcases has been repaired: ', len(repairedTests), repairedTests
    #===============================================================================

    '''Merge the two Xml file'''
    #===========================================================================
    #output = 'd:\\'
    #listofFailed = XmlobjFailed.get_failedtest()
    #listofRepaired = XmlobjPassed.get_isitrepaired(listofFailed)
    # listofRightval = XmlobjPassed.get_rightValues(
    #    listofRepaired,
    #    destination_root,
    #    source_root,
    #    output)
    #===========================================================================

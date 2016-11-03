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
import xmlAppGUI


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
        # THIS METHOD IS NOT LOOKING FOR DUPLICATED TESTCASES
        arr = []
        for elem in self.root:
            values = elem.findall('ATTR')
            if values[7].attrib['val'] in listofFailed and values[13].attrib['val'] == '0':
                if values[7].attrib['val'] not in arr:
                    arr.append(values[7].attrib['val'])

        return arr

    def set_rightValues(self, listofRepaired, destination_root, source_root, output):
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
                    if testnameone == testnametwo and testnameone not in fixed_test:
                        fixed_test.append(testnameone)
                        # Found the same test in the Main Report
                        # check if the structure is the same
                        source_root.remove(elemtwo)
                        destination_root.remove(elemone)
                        source_root.append(elemone)
                        destination_root.append(elemtwo)
                        counter += 1
        self.tree.write(str(output) + '\\output.xml', xml_declaration=True)
        return counter, fixed_test

    def path_leaf(self, path):
        '''Extract file name from path '''
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def testlist_creator(self, listofFailed):
        '''
        BEFORE YOU USE IT IMPORTANT !!!!!!!!!!:
        1. Create in the root directory of a program ALLE.xml what you can create by your compa framework
        when saving a testlist what contains all of the Testcases.

        Create a testlist with set of testcases what failed before
        :param string variation the name of the variation file ex:
        :param list listofFailed testcases
        '''
        row_counter = 0
        set_counter = 0
        testlist_file = ET.parse('ALLE.xml')
        testlist_root = testlist_file.getroot()
        test_status = testlist_root.findall('VARIATION-TESTLIST/TESTCONFIG/VARIATION/')
        for elem in test_status:
            if elem.tag == 'ENABLED':
                row_counter = 0
                modifier_counter = set_counter
                numof_testcases = 1 + len(elem.text) / 2
                test_states = numof_testcases * [0]
            row_counter += 1
            set_counter += 1
            if elem.text in listofFailed:
                test_states[row_counter - 2] = 1
                test_status[modifier_counter].text = str(test_states)[1:-1:]
        testlist_file.write('testlist.tl')


'''--------------------------------------Init Input Datas-------------------------------------------------------------------------------------'''
if __name__ == "__main__":

    source = ET.parse('d:\\11_ISC_Reports\\main4271.xml')

    source_root = source.getroot()
    destination = ET.parse(
        "d:\\10 ----------------Development----------------\\Python\\Xml_Parser\\Test_Files\Retested Report\\ISC_Sensor_Emulation_Unknown_XmlReport.xml")
    destination_root = destination.getroot()

    XmlobjFailed = bmwXmlApp(source, source_root)
    XmlobjPassed = bmwXmlApp(destination, destination_root)

    '''Testlist Creator'''
    listofFailed = XmlobjFailed.get_failedtest()
    XmlobjFailed.testlist_creator(listofFailed)

    ''' Failed testcases'''
    #===============================================================================
    # listofFailed = XmlobjFailed.get_failedtest()
    # print 'These are the failed testcases: ', len(listofFailed), listofFailed
    #===============================================================================

    '''Number of Duplicated Testcases(if have)'''
   # ===============================================================================
    #listofTestcases = list(XmlobjFailed.get_testnames())
    #difference = [i for i in set(listofTestcases)]
    #test = []
    # for i in listofTestcases:
    #    if i not in test:
    #        test.append(i)
    #    else:
    #        print i
    # print 'The number of duplicated testcases: ', len(listofTestcases) - len(difference)
    #===============================================================================

    '''Check for repaired Testcases'''
    #===============================================================================
    #listofFailed = XmlobjFailed.get_failedtest()
    #repairedTests = XmlobjPassed.get_isitrepaired(listofFailed)
    # print 'These testcases has been repaired: ', len(repairedTests), repairedTests
    #===============================================================================

    '''Merge the two Xml file'''

    #===========================================================================
    # output = 'd:\\'
    # listofFailed = XmlobjFailed.get_failedtest()
    # listofRepaired = XmlobjPassed.get_isitrepaired(listofFailed)
    # listofRightval = XmlobjPassed.set_rightValues(
    #     listofRepaired,
    #     destination_root,
    #     source_root,
    #     output)
    #===========================================================================

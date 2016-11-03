#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
==============================================================================
GUI for Xml Report File merging for BMW ACSM5 Proejct
==============================================================================
                            OBJECT SPECIFICATION
==============================================================================
$ProjectName: BMW ACSM5 $
$Source: xmlAppGUI.py
$Revision: 1.1 $
$Author: David Szurovecz $
$Date: 2016/10/24 16:20:32CEST $
============================================================================
"""
import Tkinter as tk
import tkMessageBox
import xmlApp
import ntpath
import time
ntpath.basename("a/b/c")
from easygui import fileopenbox, diropenbox
import xml.etree.ElementTree as ET


class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        '''Init'''
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = tk.Frame(parent)
        self.parent.pack()
        root.title('Ultimate tool for BMW ACSM5')
        self.file_one = u''
        self.file_two = u''
        self.save_list = u''
        self.initUI()

    def initUI(self):

        #=======================================================================
        # Draw the Frames
        #=======================================================================
        # Enter File Details Frame
        stepOne = tk.LabelFrame(self.parent, text=" 1. Enter File Details: ")
        stepOne.grid(row=0, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
        # OKAY Button
        stepThree = tk.Button(self.parent, text="Merge", command=self.mergeButton)
        stepThree.grid(row=3, column=0, sticky='W' + 'E', padx=5, pady=5, ipadx=20, ipady=5)
        # Step Two
        stepTwo = tk.Button(self.parent, text="Create Testlist", command=self.createList)
        stepTwo.grid(row=3, column=2, sticky='W' + 'E', padx=5, pady=5, ipadx=20, ipady=5)
        # Cancel Button
        stepFour = tk.Button(self.parent, text="Cancel", command=self.cancelbutton)
        stepFour.grid(row=3, column=1, sticky='W', padx=5, pady=5, ipadx=23, ipady=5)

        #=======================================================================
        # File Selection Text
        #=======================================================================
        inFileLbl = tk.Label(stepOne, text="Select the Main Report File: ")
        inFileLbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)
        # File Selection Entry
        self.inFileTxt = tk.Entry(stepOne)
        self.inFileTxt.grid(row=0, column=1, columnspan=7, sticky="W", pady=3)
        # File Browse Button
        inFileBtn = tk.Button(stepOne, text="Browse ...", command=self.browseFirst)
        inFileBtn.grid(row=0, column=8, sticky='W', padx=5, pady=2)

        #=======================================================================
        # File Selection 2 Text
        #=======================================================================
        inFileLbl2 = tk.Label(stepOne, text="Select the Restested Report File: ")
        inFileLbl2.grid(row=1, column=0, sticky='E', padx=5, pady=2)
        # File Selection 2 Entry
        self.inFileTxt2 = tk.Entry(stepOne)
        self.inFileTxt2.grid(row=1, column=1, columnspan=7, sticky="WE", pady=2)
        # File Save Button
        inFileBtn2 = tk.Button(stepOne, text="Browse ...", command=self.browseSecond)
        inFileBtn2.grid(row=1, column=8, sticky='W', padx=5, pady=2)

        #=======================================================================
        # Output File Path
        #=======================================================================
        outFileLbl = tk.Label(stepOne, text="Select the output path: ")
        outFileLbl.grid(row=2, column=0, sticky='E', padx=5, pady=2)
        # File Selection 2 Entry
        self.outFileTxt = tk.Entry(stepOne)
        self.outFileTxt.grid(row=2, column=1, columnspan=7, sticky="WE", pady=2)
        # File Save Button
        outFileBtn = tk.Button(stepOne, text="Browse ...", command=self.savebutton)
        outFileBtn.grid(row=2, column=8, sticky='W', padx=5, pady=2)

    def browseFirst(self):
        '''Select the files to Edit'''
        self.file_one = fileopenbox(
            default=r'd:\\',
            multiple=True)
        if self.file_one:
            for item in self.file_one:
                self.inFileTxt.insert(0, str(item.encode('utf-8')))

    def browseSecond(self):
        '''Select the files to Edit'''
        self.file_two = fileopenbox(
            default=r'd:\\',
            multiple=True)
        if self.file_two:
            for item in self.file_two:
                self.inFileTxt2.insert(0, str(item.encode('utf-8')))

    def savebutton(self):
        '''Select the files save path'''
        self.save_list = diropenbox(default=r'd:\\')
        if self.save_list:
            self.outFileTxt.insert(0, self.save_list.encode('utf-8'))

    def mergeButton(self):
        '''Input Verification and start the process'''
        if self.file_one and self.file_two and self.save_list:
            self.parse('merge')
        else:
            self.errormessage()

    def createList(self):
        if self.file_one and self.save_list:
            self.parse('testlist')
        else:
            self.errormessage()

    def cancelbutton(self):
        root.destroy()

    def errormessage(self):
        '''Show an Error window'''
        tkMessageBox.showinfo("Error", "Missing Data")

    def process(self):
        #===========================================================================
        listofRightval = xmlApp.bmwXmlApp(
            self.source,
            self.source_root).set_rightValues(
            self.listofRepaired,
            self.destination_root,
            self.source_root, self.output)
        tkMessageBox.showinfo(
            "Merge Finished", str(
                listofRightval[0]) + ' values has been modified. See Log File in the Log directory. ')
        self.logging(listofRightval)

        #===========================================================================

    def parse(self, task):
        self.source = ET.parse(self.file_one[0])
        self.source_root = self.source.getroot()
        if task == 'merge':
            self.destination = ET.parse(self.file_two[0])
            self.destination_root = self.destination.getroot()
        self.output = self.save_list
        self.listofFailed = xmlApp.bmwXmlApp(self.source, self.source_root).get_failedtest()
        if task == 'merge':
            self.listofRepaired = xmlApp.bmwXmlApp(
                self.destination,
                self.destination_root).get_isitrepaired(self.listofFailed)
            self.process()
        if task == 'testlist':
            xmlApp.bmwXmlApp(self.source_root, self.source_root).testlist_creator(self.listofFailed)

    def logging(self, listofFiles):
        timestamp = 'ACSM5_' + str(time.strftime('%Y_%m_%d_%H_%M'))
        file = open(r'Log\\' + timestamp, "w")
        file.write('Merge Finished ' + str(listofFiles[0]) + ' test cases has been modified. ')
        file.write(str(time.strftime('\n' + 'Date: ' '%Y-%m-%d:%H:%M')) + '\n')
        file.write('Main Report File          :      ' + str(self.path_leaf(str(self.file_one[0]))))
        file.write('\n' +
                   'Secondary Report File     :      ' +
                   str(self.path_leaf(str(self.file_two[0]))))
        file.write('\n' + '-' * 60 + '\n')
        [file.write(i + '\n') for i in listofFiles[1]]
        file.close()

    def path_leaf(self, path):
        '''Extract file name from path '''
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

if __name__ == "__main__":

    root = tk.Tk()
    run = MainApplication(root)
    root.mainloop()

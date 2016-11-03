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
import xml.etree.ElementTree as ET
import Tkinter as tk
import ttk as ttk
import tkMessageBox
import xmlApp
import ntpath
import time
ntpath.basename("a/b/c")
from easygui import fileopenbox, diropenbox


class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        '''Init'''
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = ttk.Notebook(parent)
        self.parent.bind_all("<<NotebookTabChanged>>", self.tabChangedEvent)
        self.tabone = tk.Frame(self.parent)
        self.tabtwo = tk.Frame(self.parent)
        self.parent.pack()
        root.title('XML Manipulator for BMW ACSM5')
        self.resetInputs()
        self.initUI()

    def tabChangedEvent(self, event):
        self.resetInputs()

    def resetInputs(self):
        self.file_one = u''
        self.file_two = u''
        self.save_list = u''

    def initUI(self):
        #=======================================================================
        # Create The Tabs
        #=======================================================================
        self.parent.add(self.tabone, text='Merging')
        self.parent.add(self.tabtwo, text='Create Testlist')
        #=======================================================================
        # Draw the Frames on Tab one
        #=======================================================================
        # Enter File Details Frame
        hintone = tk.LabelFrame(self.tabone, text=" 1. Enter File Details: ")
        hintone.grid(row=0, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
        # Merge Button
        merge_button = tk.Button(self.tabone, text="Merge", command=self.mergeButton)
        merge_button.grid(row=3, column=0, sticky='W' + 'E', padx=5, pady=5, ipadx=1, ipady=5)
        # Exit Button
        exit_button = tk.Button(self.tabone, text="Exit", command=self.cancelbutton)
        exit_button.grid(row=3, column=1, sticky='W', padx=5, pady=5, ipadx=23, ipady=5)
        #=======================================================================
        # Draw the Frames on Tab two
        #=======================================================================
        hinttwo = tk.LabelFrame(self.tabtwo, text=" 1. Enter File Details: ")
        hinttwo.grid(row=0, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
        #=======================================================================
        # File Selection 1  on Frame One
        #=======================================================================
        mergelbl_one = tk.Label(hintone, text="Select the Main Report File: ")
        mergelbl_one.grid(row=0, column=0, sticky='E', padx=5, pady=2)
        # File Selection Entry
        self.mergeent_one = tk.Entry(hintone)
        self.mergeent_one.grid(row=0, column=1, columnspan=7, sticky="W", pady=3)
        # File Browse Button
        mergebtn_one = tk.Button(hintone, text="Browse ...", command=self.browseFirst)
        mergebtn_one.grid(row=0, column=8, sticky='W', padx=5, pady=2)
        #=======================================================================
        # File Selection 2  on Frame One
        #=======================================================================
        mergelbl_two = tk.Label(hintone, text="Select the Restested Report File: ")
        mergelbl_two.grid(row=1, column=0, sticky='E', padx=5, pady=2)
        # File Selection 2 Entry
        self.mergeent_two = tk.Entry(hintone)
        self.mergeent_two.grid(row=1, column=1, columnspan=7, sticky="WE", pady=2)
        # File Save Button
        mergebtn_two = tk.Button(hintone, text="Browse ...", command=self.browseSecond)
        mergebtn_two.grid(row=1, column=8, sticky='W', padx=5, pady=2)
        #=======================================================================
        # Output File Path
        #=======================================================================
        mergelbl_three = tk.Label(hintone, text="Select the output path: ")
        mergelbl_three.grid(row=2, column=0, sticky='E', padx=5, pady=2)
        # File Selection 2 Entry
        self.mergeent_three = tk.Entry(hintone)
        self.mergeent_three.grid(row=2, column=1, columnspan=7, sticky="WE", pady=2)
        # File Save Button
        mergebtn_three = tk.Button(hintone, text="Browse ...", command=self.savebutton)
        mergebtn_three.grid(row=2, column=8, sticky='W', padx=5, pady=2)
        #=======================================================================
        # File Selection 1  on Frame Two
        #=======================================================================
        listlbl_one = tk.Label(hinttwo, text="Select the Main Report File: ")
        listlbl_one.grid(row=0, column=0, sticky='E', padx=5, pady=2)
        # File Selection 1 Entry
        self.listent_one = tk.Entry(hinttwo)
        self.listent_one.grid(row=0, column=1, columnspan=7, sticky="W", pady=3)
        # File Browse Button
        listbtn_one = tk.Button(hinttwo, text="Browse ...", command=self.browseFirst)
        listbtn_one.grid(row=0, column=8, sticky='W', padx=5, pady=2)
        #=======================================================================
        # File Selection 2  on Frame Two
        #=======================================================================
        listlbl_two = tk.Label(hinttwo, text="Select the Testlist: ")
        listlbl_two.grid(row=1, column=0, sticky='E', padx=5, pady=2)
        # File Selection 2 Entry
        self.listent_two = tk.Entry(hinttwo)
        self.listent_two.grid(row=1, column=1, columnspan=7, sticky="WE", pady=2)
        # File Save Button
        listbtn_two = tk.Button(hinttwo, text="Browse ...", command=self.browseSecond)
        listbtn_two.grid(row=1, column=8, sticky='W', padx=5, pady=2)
        #=======================================================================
        # Output File Path
        #=======================================================================
        listlbl_three = tk.Label(hinttwo, text="Select the output path: ")
        listlbl_three.grid(row=2, column=0, sticky='E', padx=5, pady=2)
        # File Selection 2 Entry
        self.listent_three = tk.Entry(hinttwo)
        self.listent_three.grid(row=2, column=1, columnspan=7, sticky="WE", pady=2)
        # File Save Button
        listbtn_three = tk.Button(hinttwo, text="Browse ...", command=self.savebutton)
        listbtn_three.grid(row=2, column=8, sticky='W', padx=5, pady=2)
        # File Testlist Button
        listbtn_four = tk.Button(self.tabtwo, text="Create Testlist", command=self.createList)
        listbtn_four.grid(row=3, column=0, sticky='W' + 'E', padx=5, pady=5, ipadx=1, ipady=5)

    def browseFirst(self):
        '''Select the files to Edit'''
        current_tab = self.parent.tab(self.parent.select(), "text")
        if current_tab == 'Merging':
            current_entry = self.mergeent_one
        elif current_tab == 'Create Testlist':
            current_entry = self.listent_one
        self.file_one = fileopenbox(
            default=r'd:\\',
            multiple=True)
        if self.file_one:
            for item in self.file_one:
                current_entry.insert(0, str(item.encode('utf-8')))

    def browseSecond(self):
        '''Select the files to Edit'''
        current_tab = self.parent.tab(self.parent.select(), "text")
        if current_tab == 'Merging':
            current_entry = self.mergeent_two
        elif current_tab == 'Create Testlist':
            current_entry = self.listent_two
        self.file_two = fileopenbox(
            default=r'd:\\',
            multiple=True)
        if self.file_two:
            for item in self.file_two:
                current_entry.insert(0, str(item.encode('utf-8')))

    def savebutton(self):
        '''Select the files save path'''
        current_tab = self.parent.tab(self.parent.select(), "text")
        if current_tab == 'Merging':
            current_entry = self.mergeent_three
        elif current_tab == 'Create Testlist':
            current_entry = self.listent_three
        self.save_list = diropenbox(default=r'd:\\')
        if self.save_list:
            current_entry.insert(0, self.save_list.encode('utf-8'))

    def mergeButton(self):
        '''Input Verification and start the process'''
        if self.file_one and self.file_two and self.save_list:
            self.parse('merge')
        else:
            self.errormessage()

    def createList(self):
        if self.file_one and self.file_two and self.save_list:
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
            xmlApp.bmwXmlApp(
                self.source_root,
                self.source_root).testlist_creator(
                self.listofFailed, self.file_two[0],
                self.output)
            tkMessageBox.showinfo('Creation Finished', 'The Testlist has been created')

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

    def progress(self):
        self.pbar = tk.Tk()
        self.pbar.title('Processing')
        pb = ttk.Progressbar(self.pbar, orient="horizontal", length=200, mode="determinate")
        pb.pack()
        pb.start()
        self.pbar.mainloop()

if __name__ == "__main__":

    root = tk.Tk()
    run = MainApplication(root)
    root.mainloop()

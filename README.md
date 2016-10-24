# XMT---XML-Merger-Tool

This tool is developed for to merge two test report from xml format.
If the first test report contains some failed testcases and you want to rerun these failed ones 
the second report will contain the passed ones what failed before. But you will have two report file what is not redundant.
Why not merge it ?  This tool help for you in that case.

Features:
- Removing failed testcases from the first tesreport what is passed in the second test report.
- Adding testcases what is passed and faied before.
- Creting a new xml what is merged.

This software code is developed in Python2.7.

Used built in libraries:
- ElementTree
- Tkinter
- Some easyGUI modules


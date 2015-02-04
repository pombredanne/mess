#!/usr/bin/env python

import sys
from qt import *
from promoter import main_form
from environment_form import env_form
from pyrpm.rpm import RPM
from pyrpm import rpmdefs
import re
import os
import shutil


DEBUG = 0
PROD_HOSTS = ['s1-noc-01', 's2-noc-01']

#========================================================


INT_TO_PPLT = 0
PP_TO_PROD = 0
DIR = ''
TO_PATH = []
RPM_REGEX = re.compile(r""".+\.rpm$""")

PACKAGES_DICT = {}

ENVIRONMENT = ""

class Promo(main_form):
    def __init__(self, parent=None, name=None, fl=0):
        main_form.__init__(self,parent,name,fl)
        
        self.connect(self.name_list, SIGNAL("selectionChanged()"), self.name_list_selectionChanged)
        self.connect(self.version_list, SIGNAL("selectionChanged()"), self.version_list_selectionChanged)
        self.connect(self.add_button, SIGNAL("clicked()"), self.add_button_clicked)
        self.connect(self.remove_button, SIGNAL("clicked()"), self.remove_button_clicked)
        self.connect(self.quit_button, SIGNAL("clicked()"), self.quit_button_clicked)
        self.connect(self.promote_button, SIGNAL("clicked()"), self.promote_button_clicked)
        
        #Get packages and populate name_list
        FILELIST = os.listdir(DIR)
        self.Get_Rpm_Package_info(FILELIST)
        
        
        #SORT THE PACKAGES, LETS TRY AND MAKE IT NEAT
        LIST_OF_PACKAGES_TO_SORT = []
        
        for PACKAGE in PACKAGES_DICT:
            
            LIST_OF_PACKAGES_TO_SORT.append(PACKAGE)
        
        LIST_OF_PACKAGES_TO_SORT.sort()
        
        for PACKAGE in LIST_OF_PACKAGES_TO_SORT:
        
            self.name_list.insertItem(PACKAGE, -1)
        
        
    def Get_Rpm_Package_info(self, FILELIST):
        
        global PACKAGES_DICT
        
        for FILE in FILELIST:
            
            try:
                
                if RPM_REGEX.match(FILE):
                    
                    FULL_FILENAME = DIR + '/' + FILE
                    rpm = RPM(file(FULL_FILENAME))
                    
                    if DEBUG > 0:
                        print "=============="
                        print "RPM Name: " + rpm.name()
                        print "Package: " + rpm.package()
                        print "Version: " + rpm[rpmdefs.RPMTAG_VERSION]
                        print "Release: " + rpm[rpmdefs.RPMTAG_RELEASE]
                        print "=============="
                    
                    
                    if PACKAGES_DICT.has_key(rpm.name()):
                        
                        if PACKAGES_DICT[rpm.name()].has_key(rpm[rpmdefs.RPMTAG_VERSION]):
                            
                            PACKAGES_DICT[rpm.name()][rpm[rpmdefs.RPMTAG_VERSION]][rpm[rpmdefs.RPMTAG_RELEASE]] = FULL_FILENAME
                        
                        else:
                            
                            PACKAGES_DICT[rpm.name()][rpm[rpmdefs.RPMTAG_VERSION]] = {}
                            PACKAGES_DICT[rpm.name()][rpm[rpmdefs.RPMTAG_VERSION]][rpm[rpmdefs.RPMTAG_RELEASE]] = FULL_FILENAME
                            
                    else:
                        
                        PACKAGES_DICT[rpm.name()] = {}
                        PACKAGES_DICT[rpm.name()][rpm[rpmdefs.RPMTAG_VERSION]] = {}
                        PACKAGES_DICT[rpm.name()][rpm[rpmdefs.RPMTAG_VERSION]][rpm[rpmdefs.RPMTAG_RELEASE]] = FULL_FILENAME
                        
                        
            except:
                pass
            
        return()
        
    
    def name_list_selectionChanged(self):
        #Get version list and populate version_list
        
        self.version_list.clear()
        self.release_list.clear()
        
        self.SELECTED_PACKAGE = str(self.name_list.currentText())
        
        VERSION_LIST_TO_SORT = []
        
        for VERSION in PACKAGES_DICT[self.SELECTED_PACKAGE]:
            
            VERSION_LIST_TO_SORT.append(VERSION)
        
        VERSION_LIST_TO_SORT.sort()
        
        for VERSION in VERSION_LIST_TO_SORT:
            
            self.version_list.insertItem(VERSION, -1)
        
        
    def version_list_selectionChanged(self):
        #Get releases and populate release_list
        
        self.release_list.clear()
        
        self.SELECTED_VERSION = str(self.version_list.currentText())
        
        RELEASE_LIST_TO_SORT = []
        
        for RELEASE in PACKAGES_DICT[self.SELECTED_PACKAGE][self.SELECTED_VERSION]:
            
            RELEASE_LIST_TO_SORT.append(RELEASE)
        
        RELEASE_LIST_TO_SORT.sort()
        
        for RELEASE in RELEASE_LIST_TO_SORT:
            
            self.release_list.insertItem(RELEASE, -1)
        
        
    def add_button_clicked(self):
        #add selected release to promote_list
             
        self.SELECTED_RELEASE = str(self.release_list.currentText())
        
        if self.SELECTED_RELEASE:
            
            self.SELECTED_FULL_FILE_NAME = PACKAGES_DICT[self.SELECTED_PACKAGE][self.SELECTED_VERSION][self.SELECTED_RELEASE]
            self.SELECTED_FILE_NAME = os.path.basename(self.SELECTED_FULL_FILE_NAME)
            
            ALREADY_EXISTS = self.promote_list.findItem(self.SELECTED_FILE_NAME)
            
            if not ALREADY_EXISTS:
                
                self.promote_list.insertItem(self.SELECTED_FILE_NAME, -1)

    def remove_button_clicked(self):
        #remove selected item from promote list
        
        SOMETHING_SELECTED = str(self.promote_list.currentText())
        
        if SOMETHING_SELECTED:
            self.promote_list.removeItem(self.promote_list.currentItem())
    
    def quit_button_clicked(self):
        #exit the application
        sys.exit()

    def promote_button_clicked(self):
        #promote the packages
        
        HOW_MANY_PACKAGES = int(self.promote_list.count())
        
        #COPY FILE TO RELEVANT REPO
        for i in range(HOW_MANY_PACKAGES):
            
            FILE = str(self.promote_list.text(i))
            
            for PATH in TO_PATH:
                
                if INT_TO_PPLT:
                    
                    shutil.copy("/var/www/html/intrepo/" + FILE, PATH)
                    
                elif PP_TO_PROD:
                    
                    for HOST in PROD_HOSTS:
                        
                        CMD = "/usr/bin/scp " + "/var/www/html/pprepo/" + FILE + " repouser@" + HOST + ":" + PATH
                        
                        RET_CODE = os.system(CMD)
                        if RET_CODE > 0:
                            print "Failed to copy files to production !!!"
                            sys.exit(1)
                            
            #CALL REPO MAINTENANCE ON THAT REPO
            if INT_TO_PPLT:
                
                CMD = "/opt/scripts/pp_repo_maint.py"
                RET_CODE = os.system(CMD)

                if RET_CODE > 0:
                    print "Create repo for PREPROD failed !!"
                    sys.exit(1)
                
                CMD = "/opt/scripts/lt_repo_maint.py"
                RET_CODE = os.system(CMD)
                
                if RET_CODE > 0:
                    print "Create repo LOAD TEST failed !!"
                    sys.exit(1)
            
            elif PP_TO_PROD:
                
                for HOST in PROD_HOSTS:
                    
                    CMD = "ssh repouser@" + HOST + " /opt/scripts/prod_repo_maint.py"
                    RET_CODE = os.system(CMD)
                
                    if RET_CODE > 0:
                        print "create repo on " + HOST + " failed !!"
                        sys.exit(1)
                        
        QMessageBox.information(self, "Packages Promoted", "All the selected packages have been promoted", QMessageBox.Ok)
        sys.exit(0)


class Env(env_form):
    def __init__(self, parent=None, name=None, fl=0):
        env_form.__init__(self,parent,name,fl)
        self.connect(self.ok_button, SIGNAL("clicked()"), self.ok_button_clicked)
       
        self.connect(self.quit_button, SIGNAL("clicked()"), self.quit_button_clicked)

    def ok_button_clicked(self):
        global DIR, TO_PATH, INT_TO_PPLT, PP_TO_PROD
        
        if self.int_to_pplt_radio.isChecked():
            
            DIR = '/var/www/html/intrepo'
            TO_PATH = ['/var/www/html/pprepo', '/var/www/html/ltrepo']
            INT_TO_PPLT = 1

        elif self.pp_to_prod_radio.isChecked():
        
            DIR = '/var/www/html/pprepo'
            TO_PATH = ['/var/www/html/prodrepo']
            PP_TO_PROD = 1
        
        QDialog.done(self, True)
        
    def quit_button_clicked(self):
        sys.exit()


if __name__ == "__main__": 
    app = QApplication(sys.argv)
    QObject.connect(app,SIGNAL("lastWindowClosed()"),app,SLOT("quit()"))
    
    #get the environment
    e = Env()
    e.exec_loop()
    
    w = Promo()
    app.setMainWidget(w)
    w.show()
    app.exec_loop()
    
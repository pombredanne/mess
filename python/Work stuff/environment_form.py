# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'environment_form.ui'
#
# Created: Tue Jun 2 11:17:30 2009
#      by: The PyQt User Interface Compiler (pyuic) 3.17.6
#
# WARNING! All changes made in this file will be lost!


from qt import *


class env_form(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("env_form")

        self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred,0,0,self.sizePolicy().hasHeightForWidth()))
        self.setMinimumSize(QSize(0,0))
        self.setModal(1)


        LayoutWidget = QWidget(self,"layout4")
        LayoutWidget.setGeometry(QRect(10,10,260,230))
        layout4 = QGridLayout(LayoutWidget,1,1,11,6,"layout4")

        self.frame8 = QFrame(LayoutWidget,"frame8")
        self.frame8.setFrameShape(QFrame.StyledPanel)
        self.frame8.setFrameShadow(QFrame.Raised)
        frame8Layout = QHBoxLayout(self.frame8,11,6,"frame8Layout")

        self.quit_button = QPushButton(self.frame8,"quit_button")
        frame8Layout.addWidget(self.quit_button)

        self.ok_button = QPushButton(self.frame8,"ok_button")
        frame8Layout.addWidget(self.ok_button)

        layout4.addWidget(self.frame8,1,0)

        self.buttonGroup1 = QButtonGroup(LayoutWidget,"buttonGroup1")
        self.buttonGroup1.setExclusive(1)
        self.buttonGroup1.setColumnLayout(0,Qt.Vertical)
        self.buttonGroup1.layout().setSpacing(6)
        self.buttonGroup1.layout().setMargin(11)
        buttonGroup1Layout = QVBoxLayout(self.buttonGroup1.layout())
        buttonGroup1Layout.setAlignment(Qt.AlignTop)

        layout3 = QVBoxLayout(None,0,6,"layout3")

        self.int_to_pplt_radio = QRadioButton(self.buttonGroup1,"int_to_pplt_radio")
        layout3.addWidget(self.int_to_pplt_radio)

        self.pp_to_prod_radio = QRadioButton(self.buttonGroup1,"pp_to_prod_radio")
        self.pp_to_prod_radio.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.pp_to_prod_radio.sizePolicy().hasHeightForWidth()))
        layout3.addWidget(self.pp_to_prod_radio)
        buttonGroup1Layout.addLayout(layout3)

        layout4.addWidget(self.buttonGroup1,0,0)

        self.languageChange()

        self.resize(QSize(279,250).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Environment ?"))
        self.quit_button.setText(self.__tr("Quit"))
        self.ok_button.setText(self.__tr("OK"))
        self.buttonGroup1.setTitle(self.__tr("Which Environment ?"))
        self.int_to_pplt_radio.setText(self.__tr("Int -> PP/LT"))
        self.pp_to_prod_radio.setText(self.__tr("PP -> Prod"))


    def __tr(self,s,c = None):
        return qApp.translate("env_form",s,c)

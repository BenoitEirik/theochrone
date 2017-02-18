#!/usr/bin/python3
# -*-coding:Utf-8 -*

import messages
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QDate, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QCalendarWidget, QComboBox, QDockWidget, QHBoxLayout, QMainWindow, QLabel, QLineEdit, QPushButton, QTableWidget, QTabWidget, QVBoxLayout, QWidget

class Main(QMainWindow):
    """Main window"""
    def __init__(self):
        """Function which initializes the main window"""
        super().__init__()
        self.actions()
        self.initUI()
        
        self.onglets.tab1.cal.clicked[QDate].connect(self.useDate)
        self.onglets.tab1.kw_bouton.clicked.connect(self.useKeyWord)
        
    def menu(self):
        """A function which describes the menubar of the main window"""
        _ = messages.main_window['menus']
        menubar = self.menuBar()
        
        # File menu
        fileMenu = menubar.addMenu(_['file'])
        fileMenu.addAction(self.exitAction)
        
        # Edit menu
        editMenu = menubar.addMenu(_['edit'])
        
        # Help menu
        helpMenu = menubar.addMenu(_['help'])
        
    def actions(self):
        """A function which defines actions in the main window"""
        _ = messages.main_window['actions']
        # Exit
        self.exitAction = QAction(QIcon('icons/exit.png'),_['exit_name'],self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip(_['exit_status'])
        self.exitAction.triggered.connect(self.close)
        
    def initUI(self):
        """A function which defines widgets and main features of the window"""
        _ = messages.main_window['init']
        # widgets
        # main widget
        tableau = QTableWidget()
        self.setCentralWidget(tableau)
        # widgets on the right
        self.rightDock = QDockWidget(_['right_dock'],self)
        self.onglets = Onglets()
        self.rightDock.setWidget(self.onglets)
        self.addDockWidget(Qt.RightDockWidgetArea,self.rightDock)
        
        # menu
        self.menu()        
        
        # statusbar
        self.statusBar()
        
        # main features
        self.setGeometry(400,400,1000,1000) # TODO centrer la fenêtre au démarrage
        self.setWindowTitle('Theochrone - ')
        self.show()
        
    def useDate(self,date):
        self.setWindowTitle('Theochrone - ' + date.toString())
        
    def useKeyWord(self):
        keyword = self.onglets.tab1.keyword.text()
        print(keyword)
        
class Onglets(QWidget):
    """A class for a tab widget"""
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
       
    def initUI(self):
        _ = messages.onglets['init']
        # main widgets
        self.tabs = QTabWidget()
        self.tab1 = Unique()
        self.tabPlus = QWidget()
        
        self.tabs.addTab(self.tab1,"1")
        self.tabs.addTab(self.tabPlus,"+")
        
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.setStatusTip(_['status'])        
        
class Unique(QWidget):
    """A class wich defines a widget with two types of research : for one date and for key-words."""
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        _ = messages.unique['init']
        self.layout = QVBoxLayout()
        
        cal_label = QLabel(_['cal_label'],self)
        self.layout.addWidget(cal_label)
        
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.setFirstDayOfWeek(0)
        self.cal.setMinimumDate(QDate(1600,1,1))
        self.cal.setMaximumDate(QDate(4100,12,31))
        #self.cal.clicked[QDate].connect(self.sendDate)
        
        self.layout.addWidget(self.cal)
        self.layout.addStretch(1)
        
        kw_label = QLabel(_['kw_label'],self)
        self.layout.addWidget(kw_label)
        
        self.keyword = QLineEdit(self)
        self.layout.addWidget(self.keyword)
        
        self.kw_bouton = QPushButton(_['kw_button'],self)
        self.layout.addWidget(self.kw_bouton)
        
        self.layout.addStretch(2)
        
        self.setLayout(self.layout)
        
        
        
        
    

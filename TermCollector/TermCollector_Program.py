"""
Term Collector Program - written by Gerri Ezeocha
Intro to Python - CSC 470
_________

This programs assists user to collect terms and defintions of a particular topic, subject, area etc
The program allows users to add as many terms/definitions, but no duplicates.
It displays terms in a List and displays each defintion as user clicks on each term.
It also allows editing of terms/definitions.
User is able to save collection of terms/definitions to a text file for each topic

"""

import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import webbrowser
import json

myData = {}
class MainPage(QMainWindow):
    def __init__(self):
        super(MainPage, self).__init__()
        loadUi('FlashCard.ui', self)
        self.myData = {}
        self.Ok_topic.clicked.connect(self.addTopic)
        self.enter_term_def.clicked.connect(self.addTermAndDef)
        self.content_view.itemClicked.connect(self.displayDef)
        self.clear_term.clicked.connect(self.clearTerm)
        self.rmv_term.clicked.connect(self.rmvTerm)
        self.edit_term.clicked.connect(self.editTerm)
        self.search_bttn.clicked.connect(self.searchTerm)
        self.download.clicked.connect(self.downLoad)
        self.clear_App.clicked.connect(self.clearApp)
        self.Exit.clicked.connect(self.closeWindow)

        
#Topic and Terms functions
    def addTopic(self):
        topic = self.topic_text.toPlainText()

        #catching an empty topic term
        msgEmpty = QMessageBox()
        msgEmpty.setIcon(QMessageBox.Information)
        msgEmpty.setText("Please Enter a Topic:")

        if topic == "":
            x = msgEmpty.exec_()
        else:
            self.topic_view.setText(topic)
        
    def addTermAndDef(self):
        term = self.termLine.text().capitalize()
        def_term = self.ent_Def.toPlainText()
        pos = -1
        found = False

        #catching empty terms/definitions
        msgEmpty = QMessageBox()
        msgEmpty.setIcon(QMessageBox.Information)
        if term == "":
            msgEmpty.setText("Please Enter a Term:")
            x = msgEmpty.exec_()
            
        elif def_term == "":
            msgEmpty.setText("Please Enter a Definition")
            x = msgEmpty.exec_()

        #Adding terms/Definitions
        elif self.content_view.count() == 0:
            self.content_view.addItem(term)
            myData[term] = def_term
        elif self.content_view.count() > 0:
            for iTem in range(self.content_view.count()):
                if term == (self.content_view.item(iTem).text()):
                    pos = self.content_view.row(self.content_view.item(iTem))
                    found = True
                    continue
            self.content_view.addItem(term)
            myData[term] = def_term
            if found == True:
                 self.content_view.takeItem(pos + 1)


    def rmvTerm(self):
        #removing term when valid and handling when invalid
        try:
            if self.content_view.count() == 0:
                return 
            else:
                item = self.content_view.currentItem()
                pos = self.content_view.row(item)
                data = self.content_view.currentItem().text()
                myData.pop(data)
                self.content_view.takeItem(pos)
                self.termView.setText(" ")
        except ValueError:
            None
                     

    def displayDef(self):
        term = self.content_view.currentItem().text()
        data = myData[term]
        self.termView.setText(data)

    def editTerm(self):
        #editing term when valid and handling when invalid
        try:
            if self.content_view.count() == 0:
                return
            else:
                term = self.content_view.currentItem().text()
                data = self.termView.toPlainText()
                self.termLine.setText(term)
                self.ent_Def.setPlainText(data)
        except ImportsError:
            None
 

        
    def clearTerm(self):
        self.termLine.clear()
        self.ent_Def.clear()
        
    
    def downLoad(self):
        #Saving data when valid and handling when invalid
        #creating and saving .txt file accordingly
        msgEmpty = QMessageBox()
        msgSaved = QMessageBox()
        msgEmpty.setIcon(QMessageBox.Warning)
        msgSaved.setIcon(QMessageBox.Information)
        msgEmpty.setText("Empty List. \nNo Term(s) Entered:")
        msgSaved.setText("Sucessfully Saved!")
        
        if self.content_view.count() == 0:
            x = msgEmpty.exec_()
        else:
            getTopic = self.topic_view.toPlainText()
            fileName = getTopic + ".txt"
            crtFile = open(fileName, "a")
            list_of_items = [f'{key} - {myData[key]}' for key in myData]
        
            with open(fileName, 'w') as file:
                 file.write("\t\t\t" + getTopic + "\n\n")
                 [file.write(f'{st}\n') for st in list_of_items]
            x = msgSaved.exec_()
                
            
    def clearApp(self):
        #clearing App when valid and handling when invalid
        try:
            if self.content_view.count() == 0:
                return
            else:        
                msgConfirm = QMessageBox()
                msgConfirm.setIcon(QMessageBox.Warning)
                msgConfirm.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
                msgConfirm.setText("Are you sure you want to Clear All?")
                x = msgConfirm.exec_()
                
                if x == QMessageBox.Ok:
                    myData.clear()
                    self.topic_view.clear()
                    self.content_view.clear()
                    self.termView.clear()
                    self.topic_text.clear()
                    self.termLine.clear()
                    self.ent_Def.clear()
                    self.search_bar.clear()
        except ValueError:
            None


#Search Browser functions
    def searchTerm(self):
        word = self.search_bar.toPlainText()
        url = 'http://www.google.com/search?hl=en&source=hp&el=LUX-XuOEEaJB0PEPjOqXyAQ&q='
        combined = url + word
        webbrowser.open(combined)
        
        
#Window function    
    def closeWindow(self):
        self.close()


       
app = QApplication(sys.argv)
widget = MainPage()
widget.show()
sys.exit(app.exec())

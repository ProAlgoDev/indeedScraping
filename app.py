import indeed
import monster
import pandas as pd
import os
import re
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QMessageBox, QLineEdit
from PyQt5.QtGui import QFont
import threading

import link


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Job_Scraping")
        self.setGeometry(100, 100, 350, 360)

        font = QFont("Arial", 14)  # Create a QFont object with Arial font and size 14

        self.skilllabel = QLabel("Input skills separated by commas", self)
        self.skilllabel.setFixedSize(300,30)
        self.skilllabel.move(20,10)
        self.skilllabel.setFont(font)

        self.skillinput = QLineEdit(self)
        self.skillinput.move(20,50)
        self.skillinput.setFixedSize(300,30)
        self.skillinput.setFont(font)
       
        
        self.locationlabel = QLabel("Input location", self)
        self.locationlabel.move(20,90)
        self.locationlabel.setFixedSize(300,30)
        self.locationlabel.setFont(font)

        self.locationinput = QLineEdit(self)
        self.locationinput.move(20,130)
        self.locationinput.setFixedSize(300,30)
        self.locationinput.setFont(font)

        self.datelabel = QLabel("Input posted date", self)
        self.datelabel.move(20,170)
        self.datelabel.setFixedSize(300,30)
        self.datelabel.setFont(font)

        self.dateinput = QLineEdit(self)
        self.dateinput.move(20,210)
        self.dateinput.setFixedSize(300,30)
        self.dateinput.setFont(font)

        self.state = QLabel("", self)
        self.state.move(120,320)
        self.state.setFixedSize(180,30)
        self.state.setFont(font)

        self.search = QPushButton("Search", self)
        self.search.setGeometry(100, 260, 150,50)
        self.search.setFont(font)
        self.search.clicked.connect(self.start_convert)

        infofont = QFont("Arial", 12)
        self.info = QPushButton("info", self)
        self.info.move(260,310)
        self.info.setStyleSheet("QPushButton { background: none; border: none; padding: 0; margin: 0; color: blue; font-style: italic;}")
        self.info.setFont(infofont)
        self.info.clicked.connect(self.contact)
    def contact(self):
       self.show_alert("If you have any questions, please contact me.\nhttps://t.me/Byte0Bandit")
    def show_alert(self,text):
        # Create a QMessageBox
        alert_text = text
        alert = QMessageBox(self)

        # Set the icon, title, and text of the QMessageBox
        alert.setIcon(QMessageBox.Information)
        alert.setWindowTitle("Alert")
        alert.setText(alert_text)

        font = alert.font()
        font.setPointSize(14)
        alert.setFont(font)

        # Add an "OK" button to the QMessageBox
        alert.setStandardButtons(QMessageBox.Ok)

        # Show the QMessageBox and handle the result
        result = alert.exec_()
        if result == QMessageBox.Ok:
            print("OK")

        
    def start_convert(self):
      location = self.locationinput.text()
      skill = self.skillinput.text()
      self.mskill = skill.split(',')
      date = self.dateinput.text()
      if location =='' or skill =='' or date =='':
       self.show_alert("Fill the blank")
      skilllist = skill.split(',')
      skill=''
      if len(skilllist) ==1:
         skill = skilllist[0]
      elif len(skilllist) >1:
        for j in skilllist:
          skill +=j
          skill +="%2C"
        skill = skill[:-3]
      startConvert = threading.Thread(target=self.start,args=(location,skill,date,))
      startConvert.daemon = True
      startConvert.start()

    def start(self,location,skill,date):
      location = location
      skill = skill
      date = date
      print(location,skill,date)
      self.state.setText("Processing...")
      # m_monster = monster.monster()
      # monster_job = m_monster.init(location,skill,date)
      # m_indeed = indeed.indeed()
      # indeed_job = m_indeed.init(location,skill,date)
      # m_link = link.link()
      # link_job  = m_link.init(location,skill,date)

      # Create threads for each function
      thread_monster = threading.Thread(target=self.run_monster, args=(location, skill, date,self.mskill,))
      thread_indeed = threading.Thread(target=self.run_indeed, args=(location, skill, date,self.mskill,))
      thread_link = threading.Thread(target=self.run_link, args=(location, skill, date,self.mskill,))

      # Start the threads
      thread_monster.start()
      thread_indeed.start()
      thread_link.start()

      # elastic search,redis,couchbase
      # Wait for all threads to finish
      thread_monster.join()
      thread_indeed.join()
      thread_link.join()
# self.indeed_job + self.monster_job+
      job = self.indeed_job+ self.monster_job+self.link_job
      # self.monster_job
      excel = "job.xlsx"
      file = open(excel,"a")
      file.close()
      df = pd.DataFrame(job)
      df = df.dropna(how='any')
      # duplicates_mask = df.duplicated(keep=False)

      # # Drop duplicated rows
      # non_duplicates_df = df[~duplicates_mask].drop_duplicates()
      df.to_excel(excel,index=False)
      print(df)
      self.state.setText("Done!")

    def run_monster(self,location, skill, date,mskill):
        self.monster_job = []
        tmpmonster = []
        for i in mskill:
          m_monster = monster.monster()
          tmpmonster = m_monster.init(location, skill, date,i)
          self.monster_job+=tmpmonster
          # Your processing with monster_job

    def run_indeed(self,location, skill, date,mskill):
        self.indeed_job = []
        for j in mskill:
          m_indeed = indeed.indeed()
          tmppindeed = m_indeed.init(location, skill, date,j)
          self.indeed_job+=tmppindeed
        # Your processing with indeed_job

    def run_link(self,location, skill, date,mskill):
        self.link_job = []
        tmplink = []
        for h in mskill:
          m_link = link.link()
          tmplink = m_link.init(location, skill, date,h)
          self.link_job+=tmplink
        # Your processing with link_job



    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
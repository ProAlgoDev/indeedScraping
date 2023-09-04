import indeed
import monster
import pandas as pd
import threading
import tkinter as tk
import link
from tkinter import messagebox
import argparse



monster_job = []
link_job = []
indeed_job = []
def start_convert():
  location = locationinput.get()
  skill = skillinput.get()
  mskill = skill.split(',')
  date = dateinput.get()
  if skill =='':
    show_alert("Fill the blank")
    return
  skilllist = skill.split(',')
  skill=''
  if len(skilllist) ==1:
      skill = skilllist[0]
  elif len(skilllist) >1:
    for j in skilllist:
      skill +=j
      skill +="%2C"
    skill = skill[:-3]
  startConvert = threading.Thread(target=start,args=(location,skill,date,mskill,))
  startConvert.daemon = True
  startConvert.start()
def show_alert(msg):
   messagebox.showerror("Error", msg)
   
def start(location,skill,date,mskill):
  location = location
  skill = skill
  date = date
  mskill = mskill
  statev.set("Processing...")

  thread_monster = threading.Thread(target=run_monster, args=(location, skill, date, mskill,))
  thread_indeed = threading.Thread(target=run_indeed, args=(location, skill, date, mskill,))
  thread_link = threading.Thread(target=run_link, args=(location, skill, date, mskill,))

  thread_monster.start()
  thread_indeed.start()
  thread_link.start()
  thread_monster.join()
  thread_indeed.join()
  thread_link.join()

  job =monster_job + indeed_job + link_job
  excel = "job.xlsx"
  file = open(excel,"a")
  file.close()
  df = pd.DataFrame(job)
  df = df.dropna(how='any')
  df.to_excel(excel,index=False)
  statev.set("Done!")

def run_monster(location, skill, date,mskill):
    global monster_job
    tmpmonster = []
    for i in mskill:
      m_monster = monster.monster()
      tmpmonster = m_monster.init(location, skill, date,i)
      monster_job+=tmpmonster

def run_indeed(location, skill, date,mskill):
    global indeed_job
    tmppindeed = []
    for j in mskill:
      m_indeed = indeed.indeed()
      tmppindeed = m_indeed.init(location, skill, date,j)
      indeed_job+=tmppindeed

def run_link(location, skill, date,mskill):
    global link_job
    tmplink = []
    for h in mskill:
      m_link = link.link()
      tmplink = m_link.init(location, skill, date,h)
      link_job+=tmplink
appp = tk.Tk()
appp.title("Job_Scraping")
appp.geometry("350x360")
font = ("Arial", 20)

skilllabel = tk.Label(appp, text="Input skills separated by commas",font=font)
skilllabel.place(x=20,y=10)
skillinput = tk.Entry(appp, font=font, width=25)
skillinput.place(x=20, y=50)

locationlabel = tk.Label(appp, text="Input location",font=font)
locationlabel.place(x=20,y=90)
locationinput = tk.Entry(appp, font=font, width=25)
locationinput.place(x=20, y=130)

datelabel = tk.Label(appp, text="Input date",font=font)
datelabel.place(x=20,y=170)
dateinput = tk.Entry(appp, font=font, width=25)
dateinput.place(x=20, y=210)

statev = tk.StringVar()
statelabel = tk.Label(appp,textvariable=statev, font=font)
statelabel.place(x=120,y=320)

search = tk.Button(appp, text="Search", font=font, width=6, height=1, command=start_convert)
search.place(x=120,y=260)
appp.mainloop()

# import keyword
import undetected_chromedriver as uc
from selenium import webdriver
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time




import pandas as pd
import openpyxl

class monster():
    def init(self,location,skill,date,mskill):
        self.mskill = mskill
        location = location
        skill = skill
        if date == '':
            recent = ''
        try:
            date = int(date)
            if date == 1:
                recent = "today"
            if date >2 and date <=7:
                recent = "last+week"
            if date >7 and date <= 14:
                recent = "last+2+weeks"
            if date >14 and date <=30:
                recent ="last+month"
            if date>30:
                recent =""
        except: 
            pass
        
        print(recent)
        search_url = f"https://www.monster.fr/emploi/recherche?q={self.mskill}&where={location}&page=1&recency={recent}&so=m.h.s"
        self.job= []
        op = uc.ChromeOptions()
        op.add_experimental_option("excludeSwitches", ["enable-automation"])
        op.add_experimental_option('useAutomationExtension', False)
        custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        op.add_argument("--disable-blink-feature=AutomationControlled")
        op.add_argument(f'--user-agent={custom_user_agent}')
        

        self.driver = webdriver.Chrome(options=op)
        self.driver.maximize_window()
        self.driver.execute_script(
                    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.get(search_url)
        time.sleep(1)
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@id='onetrust-accept-btn-handler']"))).click()
        except: pass
        self.active_flag = True
        self.driver.get(search_url)
        time.sleep(2)
        try:
          WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"//button[@aria-label='Rechercher']"))).click()
        except: pass
        try:
            self.job_fetch()
        except: 
            pass
            self.driver.quit()
        self.driver.quit()
        return self.job
    def job_fetch(self):
        divpanel = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='card-scroll-container']")))
        panel = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='sc-harTkY jEHPnr']")))
        time.sleep(3)
        while True:
            total_height = int(self.driver.execute_script("return arguments[0].scrollHeight", divpanel))
            for i in range(0,total_height,10):
                self.driver.execute_script(f"arguments[0].scrollBy(0, {i});", divpanel)
            time.sleep(15)
            currentValue = int(self.driver.execute_script(f"return arguments[0].scrollTop;", divpanel))
            total_height = int(self.driver.execute_script("return arguments[0].scrollHeight", divpanel))
            client_height = int(self.driver.execute_script("return arguments[0].clientHeight", divpanel))
            total = total_height
            currenHeight = client_height + currentValue
            check = True
            if currenHeight == total:
                while check:
                    try:
                        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".hYqokn, .hYqokn:visited"))).click()
                        currentValue = int(self.driver.execute_script(f"return arguments[0].scrollTop;", divpanel))
                        total_height = int(self.driver.execute_script("return arguments[0].scrollHeight", divpanel))
                        client_height = int(self.driver.execute_script("return arguments[0].clientHeight", divpanel))
                        total = total_height
                        currenHeight = client_height + currentValue
                        self.driver.execute_script(f"arguments[0].scrollBy(0, {currenHeight});", divpanel)
                        time.sleep(1)
                    except:
                        check = False
            if check == False:
                break
                
        joblist = divpanel.find_elements(By.TAG_NAME, "li")
        self.driver.implicitly_wait(30)
        for i in joblist:
            monsterJob={}
            try:
              adata = i.find_element(By.XPATH, ".//a[@data-testid='jobTitle']")
              if adata.text !='':
                monsterJob["title"] = adata.text
                monsterJob["skill"] = self.mskill
                monsterJob["site_name"]="Monster"
                monsterJob["job_link"]= adata.get_attribute('href')
                monsterJob["company"]= i.find_element(By.XPATH, ".//span[@data-testid='company']").text
                monsterJob["location"]= i.find_element(By.XPATH, ".//span[@data-testid='jobDetailLocation']").text
                monsterJob["post_date"]= i.find_element(By.XPATH, ".//span[@data-testid='jobDetailDateRecency']").text
                print("title------",monsterJob["title"])
                print("job_link------",monsterJob["job_link"])
                print("company------",monsterJob["company"])
                print("location------",monsterJob["location"])
                print("post_date------",monsterJob["post_date"])
                self.job.append(monsterJob)
            except:pass


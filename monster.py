
from asyncio.windows_events import NULL
from base64 import standard_b64decode
# import keyword
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time




import pandas as pd
import openpyxl

class monster():
    def init(self,location,skill,date):
        location = location
        skill = skill
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
            recent ="last+month"
        print(recent)
        # search_url = "https://www.monster.fr/emploi/recherche?q=python&where=paris&page=1&recency=today&so=m.h.s"
        # recency=last+2+days
        # recency=last+week
        # last+2+weeks
        # recency=last+month
        # %2Creact
        search_url = f"https://www.monster.fr/emploi/recherche?q={skill}&where={location}&page=1&recency={recent}&so=m.h.s"
        self.job= []
        op = uc.ChromeOptions()
        custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        op.add_argument("--disable-blink-feature=AutomationControlled")
        op.add_argument(f'--user-agent={custom_user_agent}')
        op.add_argument(f'--headless={True}')

        self.driver = uc.Chrome(options=op)

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
        self.job_fetch()
        self.driver.quit()
        return self.job
    
    def job_fetch(self):
        divpanel = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='card-scroll-container']")))
        panel = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='sc-harTkY jEHPnr']")))
        time.sleep(3)
        scroll_amount = 50  # Adjust this value as needed

        total_height = int(self.driver.execute_script("return arguments[0].scrollHeight", divpanel))
        count = 0
        while True:
            # Scroll down by scroll_amount pixels
            self.driver.execute_script(f"arguments[0].scrollBy(0, {scroll_amount});", divpanel)
            count +=1
            # Pause for a short duration to allow content to load
            self.driver.implicitly_wait(10)
            
            # Break the loop if you've reached the bottom of the content
            if count >= total_height:
                break
        self.driver.implicitly_wait(5)
        joblist = divpanel.find_elements(By.TAG_NAME, "li")
        for i in joblist:
            monsterJob={}
            try:
              adata = i.find_element(By.XPATH, ".//a[@data-testid='jobTitle']")
              if adata.text !='':
                monsterJob["title"] = adata.text
                monsterJob["site_name"]="Monster"
                monsterJob["job_link"]= adata.get_attribute('href')
                monsterJob["company"]= i.find_element(By.XPATH, ".//span[@data-testid='company']").text
                monsterJob["location"]= i.find_element(By.XPATH, ".//span[@data-testid='jobDetailLocation']").text
                monsterJob["post_date"]= i.find_element(By.XPATH, ".//span[@data-testid='jobDetailDateRecency']").text
                self.job.append(monsterJob)
            except:pass
        

# instance = monster()
# job = instance.init()
# for i in job:
#     print(i)
# input("f")
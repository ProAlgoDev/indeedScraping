import undetected_chromedriver as uc
from selenium import webdriver
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class link():
    def init(self,location,skill,date,mskill):
        self.mskill = mskill
        location = location
        skill = skill
        if date == '':
            recent = ''
        try:
            date = int(date)
            if date ==1:
                recent =86400
            if date > 1 and date <= 7:
                recent = 604800
            if date > 7 and date <= 30:
                recent = 2592000
        except: pass
       
        search_url = f"https://fr.linkedin.com/jobs/search?keywords={self.mskill}&location={location}&position=1&f_TPR=r{recent}&pageNum=0"
        self.job= []
        op = uc.ChromeOptions()
        op.add_experimental_option("excludeSwitches", ["enable-automation"])
        op.add_experimental_option('useAutomationExtension', False)
        custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        op.add_argument("--disable-blink-feature=AutomationControlled")
        op.add_argument(f'--user-agent={custom_user_agent}')
        op.add_argument(f'--headless={True}')

        self.driver = webdriver.Chrome(options=op)
        self.driver.set_window_size(600, 900)
        # self.driver.maximize_window()
        self.driver.execute_script(
                    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.get(search_url)
        time.sleep(1)
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@action-type='ACCEPT']"))).click()
        except: pass
        self.active_flag = True
        self.driver.get(search_url)
        time.sleep(2)
        try:
            self.job_fetch()

        except:
            pass
            self.driver.quit()
        self.driver.quit()
        return self.job 
    
    def job_fetch(self):
        divpanel = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='base-serp-page__content']")))
        panel = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='jobs-search__results-list']")))

        while True:
            total_height = int(self.driver.execute_script("return document.body.scrollHeight"))
            current_height = int(self.driver.execute_script("return window.scrollY;"))
            temp1 = current_height
            
            for i in range(0,total_height,10):
                self.driver.execute_script(f"window.scrollBy(0, {i});")
            time.sleep(1)
            current_height = int(self.driver.execute_script("return window.scrollY;"))
            temp2 = current_height
            if temp2 == temp1:
                break
           
        self.driver.implicitly_wait(5)
        try:
            checknext=False
            while not checknext:
                print("continue")
                WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='main-content']/section/button"))).click()
                c_height = int(self.driver.execute_script("return window.scrollY;"))
                t_height = int(self.driver.execute_script("return document.body.scrollHeight"))
                tmep1 = c_height
                step = int(tmep1/10)
                time.sleep(1.2)
                for j in range(0,t_height,step):
                    self.driver.execute_script(f"window.scrollTo(0, {j});")
        except:     
            print("next")
            checknext = True
            pass
        joblist = panel.find_elements(By.TAG_NAME, "li")
        self.driver.implicitly_wait(30)
        for i in joblist:
            monsterJob={}
            try:
              adata = i.find_element(By.XPATH, ".//a[@data-tracking-control-name='public_jobs_jserp-result_search-card']")
              if adata.text !='':
                monsterJob["title"] = adata.text
                monsterJob["skill"] = self.mskill
                monsterJob["site_name"]="LinkedIn"
                monsterJob["job_link"]= adata.get_attribute('href')
                monsterJob["company"]= i.find_element(By.XPATH, ".//h4[@class='base-search-card__subtitle']").text
                monsterJob["location"]= i.find_element(By.XPATH, ".//span[@class='job-search-card__location']").text
                monsterJob["post_date"]= i.find_element(By.TAG_NAME, "time").text
                self.job.append(monsterJob)
            except:pass
        


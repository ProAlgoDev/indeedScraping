import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class indeed(): 
    def init(self,location,skill,date,mskill):
        self.count = 1  
        self.mskill = mskill
        location = location
        skill=skill
        m_date = ''
        if date =='':
            m_date = date
        try:
            date = int(date)
            if date ==1:
                m_date = 1
            if date > 1 and date <= 3:
                m_date = 3
            if date > 3 and date <=7:
                m_date = 7
            if date >7 and date <=14:
                m_date = 14
            if date >14 and date <=30:
                m_date = 'last'
            if date > 30:
                m_date = ''
        except: pass
        print(date)
        
        self.job= []
        op = uc.ChromeOptions()
        custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        op.add_argument("--disable-blink-feature=AutomationControlled")
        op.add_argument(f'--user-agent={custom_user_agent}')
        op.add_argument(f'--headless={True}')

        self.driver = uc.Chrome(options=op)

        self.driver.execute_script(
                    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


        search_url = f"https://fr.indeed.com/jobs?q={self.mskill}&l={location}&fromage={m_date}"
        self.driver.get(search_url)
        time.sleep(1)
        try:
            iframe = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            self.driver.switch_to.frame(iframe)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']"))).click()
            self.driver.switch_to.window(self.driver.window_handles[0])
        except: 
            pass
        self.driver.get(search_url)
        self.active_flag = True
        self.driver.get(search_url)
        time.sleep(2)
        try:
            WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH, "//button[@id='onetrust-accept-btn-handler']"))).click()
        except: pass
        try:
            self.job_fetch()
            while self.active_flag:
                time.sleep(2)
                try:
                    self.job_fetch()
                except: pass
        except:
            pass
            print("")
            self.driver.quit()
        self.driver.quit()
        return self.job
    def job_fetch(self):

        left = WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".jobsearch-LeftPane")))
        data = WebDriverWait(left,10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'li')))
        for i in data:
            indeedjob = {}
            try:
                adata = i.find_element(By.TAG_NAME, 'a')
                # adata = i.find_element(By.TAG_NAME, 'a')
                jobtitle = adata.get_attribute("id")
                print(jobtitle)
                if jobtitle == '':
                    try:
                        check = self.driver.find_element(By.XPATH, "//h3[@class='DesktopJobAlertPopup-heading']")
                        if check:
                            WebDriverWait(self.driver,4).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='fermer']"))).click()
                    except: pass
                if jobtitle[:3] == "job" and jobtitle != '':
                    indeedjob["title"] = adata.text
                    indeedjob["skill"] = self.mskill
                    indeedjob["site_name"] = "Indeed"
                    indeedjob["job_link"] = adata.get_attribute("href")
                    indeedjob["company"] = i.find_element(By.XPATH, ".//span[@class='companyName']").text
                    indeedjob["location"]= i.find_element(By.XPATH, ".//div[@class='companyLocation']").text
                    tmp_date = i.find_element(By.XPATH, ".//div[@class='heading6 tapItem-gutter result-footer']/span[@class='date']").text
                    indeedjob["post_date"] = tmp_date[6:]
                    print("title------",indeedjob["title"])
                    print("job_link------",indeedjob["job_link"])
                    print("company------",indeedjob["company"])
                    print("location------",indeedjob["location"])
                    print("post_date------",indeedjob["post_date"])

                    self.job.append(indeedjob)
            except:pass
        try: 
            self.count+=1
            print(self.count)
           
            time.sleep(.6)
            next = self.driver.find_element(By.XPATH, f"//a[@data-testid='pagination-page-{self.count}']")
            nexturl = next.get_attribute('href')
            self.driver.get(nexturl)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        except: 
            self.active_flag = False
            pass


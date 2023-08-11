
from asyncio.windows_events import NULL


import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


import pandas as pd


class indeed():   
    def init(self,location,skill,date):
        location = location
        skill=skill
        date = int(date)

        self.job= []
        op = uc.ChromeOptions()
        custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        op.add_argument("--disable-blink-feature=AutomationControlled")
        op.add_argument(f'--user-agent={custom_user_agent}')
        op.add_argument(f'--headless={True}')

        self.driver = uc.Chrome(options=op)

        self.driver.execute_script(
                    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


        # search_url = "https://fr.indeed.com/jobs?q=python%2Creact%2Cphp&l=Paris&fromage=1"
        search_url = f"https://fr.indeed.com/jobs?q={skill}&l={location}&fromage={date}"
        self.driver.get(search_url)
        time.sleep(1)
        try:
            iframe = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            self.driver.switch_to.frame(iframe)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']"))).click()
            self.driver.switch_to.window(self.driver.window_handles[0])
        except: 
            pass
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
                self.job_fetch()
        except:
            pass
        self.driver.quit()
        return self.job
    def job_fetch(self):

        left = WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".jobsearch-LeftPane")))
        data = WebDriverWait(left,10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'li')))
        for i in data:
            indeedjob = {}
            try:
                adata = i.find_element(By.TAG_NAME, 'a')
                jobtitle = adata.get_attribute("id")
                print(jobtitle)
                if jobtitle == '':
                    try:
                        check = self.driver.find_element(By.XPATH, "//h3[@class='DesktopJobAlertPopup-heading']")
                        if check:
                            print("ohmyugold")

                            WebDriverWait(self.driver,4).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='fermer']"))).click()
                    except: pass
                if jobtitle[:3] == "job" and jobtitle != '':
                    indeedjob["title"] = adata.text
                    indeedjob["site_name"] = "Indeed"
                    indeedjob["job_link"] = adata.get_attribute("href")
                    indeedjob["company"] = i.find_element(By.XPATH, ".//span[@class='companyName']").text
                    indeedjob["location"]= i.find_element(By.XPATH, ".//div[@class='companyLocation']").text
                    # try:
                    #     indeedjob["salary"] = i.find_element(By.XPATH, ".//div[@data-testid='attribute_snippet_testid']").text
                    # except:
                    #     indeedjob["salary"] = i.find_element(By.XPATH, ".//span[@class='estimated-salary']").text
                    #     pass
                    tmp_date = i.find_element(By.XPATH, ".//div[@class='heading6 tapItem-gutter result-footer']/span[@class='date']").text
                    indeedjob["post_date"] = tmp_date[6:]
                    # print("title------",indeedjob["title"])
                    # print("job_link------",indeedjob["job_link"])
                    # print("company------",indeedjob["company"])
                    # print("location------",indeedjob["location"])
                    # print("post_date------",indeedjob["post_date"])
                    # print("salary------",indeedjob["salary"])
                    # adata.click()

                    # right = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".jobsearch-RightPane")))
                    # try:
                    #     r_company_link=''
                    #     r_company_link = WebDriverWait(right,6).until(EC.presence_of_element_located((By.XPATH, ".//div[@data-testid='inlineHeader-companyName']/span/a"))).get_attribute('href')
                    #     # rdata = right.find_element(By.XPATH, "//div[@testid='inlineHeader-companyName']/span/a")
                    #     print("company_link----",r_company_link)
                    #     indeedjob["company_link"] = r_company_link
                    # except:
                    #     pass
                    # try:
                    #     tmp_jobdescription_p = WebDriverWait(right,30).until(EC.presence_of_element_located((By.XPATH, ".//div[@id='jobDescriptionText']")))
                    #     print("ttttt",tmp_jobdescription_p)
                    #     tmp_jobdescription_ptags = WebDriverWait(tmp_jobdescription_p, 30).until(EC.presence_of_all_elements_located((By.XPATH, ".//*")))
                    #     tmp_des_text=''
                    #     for j in tmp_jobdescription_ptags:
                    #         if j.text:
                    #             tmp_des_text += j.text
                    #             print(j.text)
                    #     indeedjob["job_description"] = tmp_des_text
                    # except: pass
                    
                    self.job.append(indeedjob)
            except:pass
            time.sleep(.2)
        try: 
            next = WebDriverWait(left, 10).until(EC.element_to_be_clickable((By.XPATH, ".//a[@data-testid='pagination-page-next']")))
            next.click()

        except: 
            
            self.active_flag = False
            pass


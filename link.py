
from asyncio.windows_events import NULL
from base64 import standard_b64decode
# import keyword
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


class link():
    def init(self,location,skill,date):
        location = location
        skill = skill
        date = int(date)
        recent = 3600*24*date
        # search_url = "https://www.monster.fr/emploi/recherche?q=python&where=paris&page=1&recency=today&so=m.h.s"
        # recency=last+2+days
        # recency=last+week
        # last+2+weeks
        # recency=last+month
        # %2Creact
        # https://fr.linkedin.com/jobs/search?keywords=php%2Creact&location=paris&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0
        # https://fr.linkedin.com/jobs/search?keywords=Php&location=Paris%2C%20%C3%8Ele-de-France%2C%20France&locationId=&geoId=101240143&f_TPR=r86400&distance=25&position=1&pageNum=0
        # https://fr.linkedin.com/jobs/search?keywords=Php&location=Paris%2C%20%C3%8Ele-de-France%2C%20France&locationId=&geoId=101240143&f_TPR=r604800&distance=25&position=1&pageNum=0
        # https://fr.linkedin.com/jobs/search?keywords=php&location=paris&position=1&pageNum=0
        # https://fr.linkedin.com/jobs/search?keywords=Php&location=Paris%2C%20%C3%8Ele-de-France%2C%20France&locationId=&geoId=101240143&f_TPR=r86400&distance=25&position=1&pageNum=0
        # https://fr.linkedin.com/jobs/search?keywords=Php&location=Paris%2C%20%C3%8Ele-de-France%2C%20France&locationId=&geoId=101240143&f_TPR=r604800&distance=25&position=1&pageNum=0
        # https://fr.linkedin.com/jobs/search?keywords=Php&location=Paris%2C%20%C3%8Ele-de-France%2C%20France&locationId=&geoId=101240143&f_TPR=r2592000&distance=25&position=1&pageNum=0

        search_url = f"https://fr.linkedin.com/jobs/search?keywords={skill}&location={location}&position=1&f_TPR=r{recent}&pageNum=0"
        self.job= []
        op = uc.ChromeOptions()
        custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        op.add_argument("--disable-blink-feature=AutomationControlled")
        op.add_argument(f'--user-agent={custom_user_agent}')
        op.add_argument(f'--headless={True}')

        self.driver = uc.Chrome(options=op)
        self.driver.set_window_size(600, 400)
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
        self.job_fetch()
        self.driver.quit()

        return self.job
    
    def job_fetch(self):
        divpanel = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='base-serp-page__content']")))
        panel = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='jobs-search__results-list']")))

        scroll_amount = 50  # Adjust this value as needed
       
        total_height = int(self.driver.execute_script("return document.body.scrollHeight"))
        count = 0
        while True:
            # Scroll down by scroll_amount pixels
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            count +=1
            # Pause for a short duration to allow content to load
            self.driver.implicitly_wait(10)
            
            # Break the loop if you've reached the bottom of the content
            if count >= total_height:
                break
        self.driver.implicitly_wait(5)

        joblist = panel.find_elements(By.TAG_NAME, "li")
        for i in joblist:
            monsterJob={}
            try:
              adata = i.find_element(By.XPATH, ".//a[@data-tracking-control-name='public_jobs_jserp-result_search-card']")
              if adata.text !='':
                monsterJob["title"] = adata.text
                monsterJob["site_name"]="LinkedIn"
                monsterJob["job_link"]= adata.get_attribute('href')
                monsterJob["company"]= i.find_element(By.XPATH, ".//h4[@class='base-search-card__subtitle']").text
                monsterJob["location"]= i.find_element(By.XPATH, ".//span[@class='job-search-card__location']").text
                monsterJob["post_date"]= i.find_element(By.TAG_NAME, "time").text
                self.job.append(monsterJob)
            except:pass
        


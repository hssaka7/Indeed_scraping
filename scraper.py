import time

import pandas as pd

import logging
from selenium import webdriver
from selenium.webdriver.common.by import By

from utils import url_builder
from worker import Worker

logging.basicConfig(level=logging.INFO)


class IndeedScraper(Worker):
    
    def get_jobboards(self,job_title, location):
        """parse the HTML and returns the data needed from the job boad page. It mimics the human behavior"""
        url = url_builder(job_title=job_title, location=location)
        driver = webdriver.Chrome()
        driver.get(url)

        jobs = []
        has_next = True
        count = 1
        while has_next:
            
            time.sleep(2)
            cards = driver.find_elements(By.CLASS_NAME,'cardOutline')
            for card in cards:
                job_title = card.find_element(By.CLASS_NAME,'jobTitle')
                job_title_text = job_title.text
                job_id = job_title.find_element(By.TAG_NAME, 'a').get_attribute('data-jk')
                location = card.find_element(By.CLASS_NAME,'company_location').text
                job_description = card.find_element(By.CLASS_NAME,'underShelfFooter').text
                
                try:
                    pay,*_metadata = card.find_element(By.CLASS_NAME,'heading6').text.split('\n')
                except Exception as e:
                    pay = 'NA'
                    _metadata = []
            
                
                jobs.append({
                    'job_title':job_title_text,
                    'location': location,
                    'description': job_description,
                    'pay rate': pay,
                    'metadata': _metadata,
                    'job_id':job_id,
                    'job_url': f"https://www.indeed.com/viewjob?jk={job_id}",
                    
                })

            try:
                driver.find_element(By.CSS_SELECTOR,"[data-testid='pagination-page-next']").click()
                count += 1
            except Exception as e:
                print(f"Ending at page {count}")
                has_next = False
        logging.info(f"Total pages scraped: {count}")
        driver.close()
        return jobs

    def run(self):
        logging.info("Running Indeed scraper")
        job_title = self.config['job_title']
        location = self.config['location']
        jobs = self.get_jobboards(job_title=job_title, location=location)
        df = pd.DataFrame(jobs)
        # TODO: add date and time to the file name
        self.save_result(file_name=f"{job_title}_{location}.csv",content=df.to_csv())
        
        return True

    def test(self):
        logging.info("Test successfull")
        return True


if __name__ == "__main__":
    extract_config = [
        {'name': 'indeed_exrtract', 'job_title':'Python Developer', 'location':'Fort Worth, TX'},
        {'name': 'indeed_exrtract', 'job_title':'Python Developer', 'location':'Albuquerque, NM'},
        # {'name': 'indeed_exrtract', 'job_title':'Python Developer', 'location':'Chicago, IL'},
        # {'name': 'indeed_exrtract', 'job_title':'Python Developer', 'location':'Miami, FL'},


    ]

    extract_objs = [IndeedScraper(**_config) for _config in extract_config]
    print([obj.run() for obj in extract_objs])






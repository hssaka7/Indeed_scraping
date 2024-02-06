import os

from abc import ABC, abstractmethod
import logging
from selenium import webdriver

from utils import url_builder

logging.basicConfig(level=logging.INFO)

class Worker(ABC):
    """
    This class needs to be implemented by each scrapper or loader, so that common features can be reused easly.
    The worker subclass needs to implement run method to implement the strategy for the worker.
    """

    def __init__(self,*args, **kwargs):
        self.name = kwargs['name']
        self.config = kwargs
        

    def _create_workspace(self):
        self.worker_dir = f"{self.name}"
        os.mkdir(self.worker_dir)

    def _setup(self):
        self._create_workspace(self)


    @abstractmethod
    def run():
        pass


class IndeedScraper(Worker):
    
    def get_jobboards(self,url):
        """parse the HTML and returns the data needed from the job boad page. It mimics the human behavior"""
        driver = webdriver.Chrome()
        

        
    
    def run(self):
        job_title = self.config['job_title']
        location = self.config['location']
        self.url = url_builder(job_title=job_title, location=location)
        logging.info(f"Extracting {self.url}")
        job_boards = self.get_jobboards(self.url)

        # Get Url
        # parse the url to get the jobs details and apply url link
        # parse each page until next button dissapears

        


    

if __name__ == "__main__":
    extract = IndeedScraper(name = 'extract',job_title = 'Python Developer', location='Fort Worth, TX')
    extract.run()




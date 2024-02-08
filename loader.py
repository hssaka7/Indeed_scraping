import logging
import pandas as pd
from worker import Worker

logging.basicConfig(level=logging.INFO)

class IndeedLoader(Worker):
    """This class will read the scraped data and loads it to the db"""
    
    def run(self,feed_name):
        logging.info("Running Indeed data loader")
        if feed_name != self.name:
            raise Exception(f"feed name: {feed_name}, does not match with loader {self.name}")
        
        # Load to sqlite db
       
        
        read_file_path = f"{feed_name}/{self.worker_id}"
        file_paths = self.get_scraped_file_paths(read_file_path)
        
        logging.info(file_paths)

        self.insert_worker_table(status = 'loading')
        
        # TRANSFORM LOGIC
        for fp in file_paths:
            df = pd.read_csv(fp)
            df2 = pd.melt(df, id_vars=['job_id'], 
              value_vars=['company_name', 'job_title', 'location', 'job_type','description', 'pay_rate', 'job_url','rating'],
              var_name='key_name', value_name='value')
            

        
        self.insert_worker_table(status= 'loaded')


if __name__ == "__main__":
    loader  = IndeedLoader(name= 'indeed', worker_id = 20240207201810772526)
    loader.run(feed_name='indeed')
import logging
import pandas as pd
from worker import Worker

logging.basicConfig(level=logging.INFO)

class IndeedLoader(Worker):
    """This class will read the scraped data and loads it to the db"""
    
    def run(self):
        # Load to sqlite db
        logging.info("Running Indeed data loader")
        
        file_paths = self.get_scraped_file_paths(self.config['file_path'])
        
        logging.info(file_paths)
        
        for fp in file_paths:
            df = pd.read_csv(fp)
            print(df.shape)
            print(df.head(10))
            print("========")

        


if __name__ == "__main__":
    loader  = IndeedLoader(name= 'indeed', file_path = "indeed_extract")
    loader.run()
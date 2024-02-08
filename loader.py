import logging
import pandas as pd
from worker import Worker

logging.basicConfig(level=logging.INFO)

class IndeedLoader(Worker):
    """This class will read the scraped data and loads it to the db"""
    
    def run(self):
        logging.info("Running Indeed data loader")
        
        file_paths = self.get_input_files()
        
        logging.info(file_paths)
        
        # TODO Only run if the status is extracted or there is file path
        self.insert_worker_table(status = 'loading')

        # TRANSFORM LOGIC
        for fp in file_paths:
            df = pd.read_csv(fp)
            df_melted = pd.melt(df, id_vars=['job_id'], 
              value_vars=['company_name', 'job_title', 'location', 'job_type','description', 'pay_rate', 'job_url','rating'],
              var_name='key_name', value_name='value')
            df_melted['worker_id'] = self.worker_id
            df_melted.dropna(inplace=True)
            print("melting")
            df_melted = df_melted.astype({'job_id':'string', 'key_name': 'string', 'value':'string','worker_id':'string'})
            print("adding result")
            self.add_results(df_melted)

        self.insert_worker_table(status= 'loaded')


if __name__ == "__main__":
    loader  = IndeedLoader(name= 'indeed', worker_id = '20240207201810772526')
    loader.run()
import logging
import pandas as pd
from worker import Worker

logging.basicConfig(level=logging.INFO)

class IndeedLoader(Worker):
    """This class will read the scraped data and loads it to the db"""
    
    def run(self):
        logging.info(f"Running Indeed data loader {self.worker_id}")
        
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
            df_melted = df_melted.astype({'job_id':'string', 'key_name': 'string', 'value':'string','worker_id':'string'})
           
            self.add_results(df_melted.values.tolist())

        self.insert_worker_table(status= 'loaded')
        logging.info(f"Finishing Indeed data loader {self.worker_id}...")

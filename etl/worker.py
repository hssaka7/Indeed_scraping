
import datetime
import logging 
import os
import sqlite3

from constants import FEED_MAPPING

from abc import ABC, abstractmethod


WORKER_CONFIG = {
    "workspace_location": "etl_workspace",
    "log": "logs/",
    "database": "scrapers.db",


}

logging.basicConfig(level=logging.INFO)

class Worker(ABC):
    """
    This class needs to be implemented by each scrapper or loader, so that common features can be reused easly.
    The worker subclass needs to implement run method to implement the strategy for the worker.
    """

    def __init__(self,*args, **kwargs):

        self._worker_config = WORKER_CONFIG

        # must match the feed name in FEED table
        self.name = kwargs['name']
    
        # Generate unique worker_id 
        today = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        self.worker_id = str(kwargs.get('worker_id', today))
        
        self.config = kwargs
        
        self.workspace_dir = self._create_workspace()
        

    def _create_workspace(self):
        worker_dir = f"{self._worker_config['workspace_location']}/{self.name}/{self.worker_id}"

        if not os.path.exists(worker_dir):
            logging.info(f"Creating {worker_dir}")
            os.makedirs(worker_dir)

        return worker_dir

    def save_result(self, file_name, content):
       
        file_path = f"{self.workspace_dir}/{file_name}"
        logging.info(f"Saving result to {file_path}")

        with open (file_path, 'w') as f:
            f.write(content)

    def get_input_files(self):
    
        file_path = f"{self._worker_config['workspace_location']}/{self.name}/{self.worker_id}"
        logging.info(f"Reading file path: {file_path}")
        return [f"{file_path}/{_f}" for _f in os.listdir(file_path)]
    
    def insert_worker_table(self,status):
        with sqlite3.connect(self._worker_config['database']) as conn:
            feed_id = FEED_MAPPING[self.name]['id']
            query = f"""
            INSERT or REPLACE INTO WORKER (ID, FEED_ID, STATUS)
            VALUES('{self.worker_id}','{feed_id}', '{status}');
            """
            conn.execute(query)
            logging.info(f"updated status: {status}")
        

    def add_results(self,rows):
        query = "INSERT INTO result(job_id,key_name,value,worker_id) VALUES(?,?,?,?)"
        with sqlite3.connect(self._worker_config['database']) as conn:
        
            logging.info(f"Adding {len(rows)} to result table ")
            try:
                r = conn.executemany( "INSERT INTO result(job_id,key_name,value,worker_id) VALUES(?,?,?,?)",rows)
                logging.info(f"Added {len(rows)} result {r}" )
            except Exception as e:
                logging.error(e)
               
    @abstractmethod
    def run(slef):
        pass
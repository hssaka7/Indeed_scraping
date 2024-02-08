
import datetime
import logging 
import os
import uuid

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
        today = datetime.datetime.now().strftime('%Y%m%d_%H%M%S%f')
        self.worker_id = kwargs.get('worker_id', int(today))
        
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

    def get_scraped_file_paths(self, project_path):
        file_path = f"{self._worker_config['workspace_location']}/{project_path}"
        logging.info(f"Reading file path: {file_path}")

        return [f"{file_path}/{_f}" for _f in os.listdir(file_path)]
        

    @abstractmethod
    def run():
        pass
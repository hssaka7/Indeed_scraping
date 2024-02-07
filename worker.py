
import logging 
import os

from abc import ABC, abstractmethod


WORKER_CONFIG = {
    "workspace_location": "etl_workspace",
    "log": "logs/",
    "database": "",


}

logging.basicConfig(level=logging.INFO)

class Worker(ABC):
    """
    This class needs to be implemented by each scrapper or loader, so that common features can be reused easly.
    The worker subclass needs to implement run method to implement the strategy for the worker.
    """

    def __init__(self,*args, **kwargs):

        self._worker_config = WORKER_CONFIG

        self.name = kwargs['name']
        self.config = kwargs
        
        self._setup()

        
        

    def _create_workspace(self):
        worker_dir = f"{self._worker_config['workspace_location']}/{self.name}"
        if not os.path.exists(worker_dir):
            logging.info(f"Creating workspace directory : {worker_dir}...")
            os.mkdir(worker_dir)
        return worker_dir

    def _setup(self):
        home_dir = f"{self._worker_config['workspace_location']}"
        if not os.path.exists(home_dir):
            logging.info(f"Creating home directory : {home_dir}...")
            os.mkdir(home_dir)
        
        self.workspace_dir = self._create_workspace()

    def save_result(self, file_name, content):
        file_path = f"{self.workspace_dir}/{file_name}"
        logging.info(f"Saving result to {file_path}")

        with open (file_path, 'w') as f:
            f.write(content)

    @abstractmethod
    def run():
        pass
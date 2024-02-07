import logging

from worker import Worker

logging.basicConfig(level=logging.INFO)

class IndeedLoader(Worker):
    """This class will read the scraped data and loads it to the db"""
    
    def run(self):
        # Load to sqlite db
        logging.info("Running Indeed data loader")
        logging.info("")
        pass


if __name__ == "__main__":
    loader  = IndeedLoader(name= 'load')
    loader.run()
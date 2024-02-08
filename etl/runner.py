from scraper import IndeedScraper
from loader import IndeedLoader

if __name__ == "__main__":
    extract_config = [
        {'name': 'indeed', 'job_title':'Python Developer', 'location':'Fort Worth, TX'},
        {'name': 'indeed', 'job_title':'Python Developer', 'location':'Albuquerque, NM'},
        {'name': 'indeed', 'job_title':'Python Developer', 'location':'Chicago, IL'},
        {'name': 'indeed', 'job_title':'Python Developer', 'location':'Miami, FL'},
    ]

    extract_objs = [IndeedScraper(**_config) for _config in extract_config]
    extract_results = [obj.run() for obj in extract_objs]
    
    loader_objs = [IndeedLoader(name =_name, worker_id=_worker_id) for _name, _worker_id in extract_results]
    loader_results = [obj.run() for obj in loader_objs]


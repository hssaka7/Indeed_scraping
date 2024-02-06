def url_builder(job_title, location, page_number=10 ):
    job_title = "+".join(job_title.split(" "))
    location = "+".join(location.split(" "))
    base_url = "https://www.indeed.com/jobs"
    query_str = f"?q={job_title}&l={location}"
    url = f"{base_url}{query_str}"
     
    return url
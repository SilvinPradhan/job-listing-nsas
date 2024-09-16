import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

# Function to fetch jobs from Adzuna API restricted to US
def fetch_adzuna_jobs(search_term, location=""):
    url = f"https://api.adzuna.com/v1/api/jobs/us/search/1"
    params = {
        'app_id': ADZUNA_APP_ID,
        'app_key': ADZUNA_APP_KEY,
        'results_per_page':
        5,  # Adjust this to change the number of jobs returned
        'what': search_term,
        'where': location,  # This can be a US state abbreviation
        'content-type': 'application/json'
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []

    data = response.json()
    jobs = []

    for job in data['results']:
        job_info = {
            'title': job['title'],
            'company': job['company']['display_name'],
            'location': job['location']['display_name'],
            'link': job['redirect_url']
        }
        jobs.append(job_info)

    return jobs


# Function to format job listings
def format_jobs(jobs):
    if not jobs:
        return None  # Return None if there are no jobs

    return "\n\n".join([
        f"**{job['title']}** at {job['company']} in {job['location']}\nLink: {job['link']}"
        for job in jobs
    ])
    
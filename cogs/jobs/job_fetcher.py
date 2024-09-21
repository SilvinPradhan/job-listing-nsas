import aiohttp
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

# Function to fetch jobs from Adzuna API restricted to US
def fetch_adzuna_jobs(search_term, location="",salary_min=0, company="", page=1, days_limit=30):
    url = f"https://api.adzuna.com/v1/api/jobs/us/search/{page}"
    params = {
        'app_id': ADZUNA_APP_ID,
        'app_key': ADZUNA_APP_KEY,
        'results_per_page': 5,
        'what': search_term,
        'where': location,  # This can be a US state abbreviation
        'salary_min': salary_min,
        'content-type': 'application/json'
    }
    if company:
        params['company'] = company

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []

    data = response.json()
    jobs = []

    now = datetime.now()
    time_limit = now - timedelta(days=days_limit)

    for job in data['results']:
        created_date = datetime.strptime(job['created'], '%Y-%m-%dT%H:%M:%SZ')
        if created_date >= time_limit:  # Only include jobs created within the limit
            job_info = {
                'title': job['title'],
                'company': job['company']['display_name'],
                'location': job['location']['display_name'],
                'link': job['redirect_url'],
                'created': job['created']
            }
            jobs.append(job_info)

    return jobs


# Function to fetch jobs from Adzuna API dynamically based on user input
async def fetch_jobs_from_adzuna(title, job_type, state, city):
    url = 'http://api.adzuna.com:80/v1/api/jobs/us/search/1'
    params = {
        'app_id': os.getenv('ADZUNA_APP_ID'),
        'app_key': os.getenv('ADZUNA_APP_KEY'),
        'results_per_page': 10,
        'what': title,
        'where': f"{city}, {state}",
        'content-type': 'application/json'
    }
    
    if job_type == 'full_time':
        params['full_time'] = 1
    elif job_type == 'part_time':
        params['part_time'] = 1
    elif job_type == 'permanent':
        params['permanent'] = 1
    elif job_type == 'contract':
        params['contract'] = 1
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data['results']
            return None

# Function to format job listings
def format_jobs(jobs):
    if not jobs:
        return None  # Return None if there are no jobs

    return "\n\n".join([
        f"**{job['title']}** at {job['company']} in {job['location']} (Posted on: {job['created']})\nLink: {job['link']}"
        for job in jobs
    ])   
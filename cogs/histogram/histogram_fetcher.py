import requests
import os
from dotenv import load_dotenv

load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

# Function to fetch histogram data from Adzuna API
def fetch_salary_histogram(job_title, state):
    url = f"https://api.adzuna.com/v1/api/jobs/us/histogram"
    params = {
        'app_id': ADZUNA_APP_ID,
        'app_key': ADZUNA_APP_KEY,
        'what': job_title,
        'location0': 'US',
        'location1': state,
        'content-type': 'application/json'
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None

    data = response.json()
    return data.get('histogram')

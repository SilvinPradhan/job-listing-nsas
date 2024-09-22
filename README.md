# Discord Job Bot for Internship Listings

This Discord bot is designed to fetch the latest job and internship listings using the [Adzuna Job Search API](https://developer.adzuna.com/). It can be used to search for internships by field and location, as well as automatically post job updates to a specific Discord channel every 6 hours.


## Contributing

We follow a **feature branch workflow**. All new features and bug fixes should go to the `dev` branch first.

### Workflow

1. **Fork the repository**.
2. **Create a new branch** from `dev` (e.g., `feature/new-feature`).
3. **Make your changes and commit** them to your new branch.
4. **Push your branch** to your forked repository.
5. **Submit a pull request** targeting the `dev` branch.
6. Your changes will be reviewed, and once approved, they will be merged into `dev`.
7. Periodically, `dev` will be merged into `main` after it has been tested and is stable.

### Branch Protection

- The `main` branch is **protected** and only accepts changes from the `dev` branch after thorough testing.
- All contributions must be submitted via pull requests to the `dev` branch.

Thank you for contributing!

---

## Features

- **Fetch job listings by custom keywords**: Allows users to search for jobs by custom keywords and US state codes.
- **Fetch job listings**: Allows users to search for internships in specific fields and US states, with rate-limited commands to avoid API spamming.
- **Scheduled job postings**: Automatically posts the latest job listings for predefined fields and locations at regular intervals (every 6 hours).
- **Salary histogram**: Fetches and displays the salary distribution for a specific job title and location (state) in the United States.
- **Motivational quotes**: Posts a daily motivational quote in a designated channel.
- **Rate-limited commands**: The job search commands are rate-limited to prevent API spamming.
- **Slash commands**: Uses Discord’s modern slash commands for user interaction.

## Prerequisites

- Python 3.8 or above
- A [Discord Developer Account](https://discord.com/developers/applications)
- A [Discord Bot Token](https://discord.com/developers/docs/intro)
- Adzuna API Credentials (App ID and App Key)

---

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/discord-bot.git
    cd discord-bot
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables by creating a `.env` file in the project’s root directory with the following content:

    ```env
    DISCORD_BOT_TOKEN=your_discord_bot_token
    ADZUNA_APP_ID=your_adzuna_app_id
    ADZUNA_APP_KEY=your_adzuna_app_key
    JOB_POSTING_CHANNEL_ID=your_channel_id  # The ID of the Discord channel where job listings will be posted
    ```

4. Run the bot:

    ```bash
    python job_bot.py
    ```

Once the bot is online, it will respond to slash commands and automatically post job listings.

---

## Commands

### `/job_search_by_keywords`

**Description**: Searches for jobs by custom keywords and US state codes (e.g., TX for Texas, LA for Louisiana).

**Usage**: `/job_search_by_keywords keywords:<keywords> location:<state_code>`

- **Keywords**: Enter a job title or keywords (e.g., `software engineer`, `data scientist`).
- **Location**: Enter a valid two-letter US state code (e.g., `TX` for Texas, `CA` for California).

**Example**: `/job_search_by_keywords keywords:software engineer location:TX`

This command fetches job listings based on the provided keywords and location.

---

### `/job_search_internships`

**Description**: Fetches the latest internships for a specific field and US state.

**Usage**: `/job_search_internships field:<job_field> state:<state_code>`

- **Field**: Select a field (e.g., `Computer Science`, `Biology`).
- **State**: Enter a valid US state code (e.g., `TX` for Texas, `CA` for California).

**Example**: `/job_search_internships field:Computer Science state:TX`

The command fetches internships in a specific field and location.

If there are too many job listings, the bot will split the message into multiple chunks to stay within Discord's 2000-character message limit.

**Rate Limit**: The command is rate-limited to one request per 30 seconds per user to avoid overloading the API.

---

### `/salary_histogram` Command

**Description**: Fetches and displays the salary distribution (in histogram format) for a specific job title and location (state) in the United States.

**Usage**: `/salary_histogram job_title:<job_title> state:<state_code>`

- **Job Title**: Enter any job title (e.g., `software engineer`, `data scientist`).
- **State**: Enter a valid two-letter US state code (e.g., `TX` for Texas, `LA` for Louisiana).

**Example**: `/salary_histogram job_title:software engineer state:TX`

This command fetches the salary distribution for the given job title and state, and returns a histogram displaying salary ranges and the number of vacancies in each range.

**Note**: The bot defers the response to handle long API requests and plotting time. It will return the histogram image once it has been generated.

### Motivational Quotes

The bot is configured to fetch a motivational quote from the [ZenQuotes API](https://zenquotes.io/) and post it in the designated Discord channel every 24 hours.

- **API Used**: [ZenQuotes API](https://zenquotes.io/)

**Example Output**:

```plaintext
"Your time is limited, so don't waste it living someone else's life." - Steve Jobs
```

### Automatic Job Postings

The bot is configured to automatically post job listings to a specified Discord channel every 6 hours. The default setup fetches internships for predefined job fields and locations.

- **Computer Science** internships are posted in Louisiana.
- **Biology** internships are posted in Louisiana.

**Customizing Auto Postings**:
You can modify the code in the `post_jobs()` function (found in `bot.py`) to change the job fields and locations for automatic postings.

---

## File Structure

```plaintext
JOB_BOT/
├── cogs/                     
│   ├── excel/                
│   │   ├── __init__.py
│   │   ├── excel_formatting.py
│   │   ├── excel_generator.py
│   ├── histogram/            
│   │   ├── __init__.py
│   │   ├── histogram_fetcher.py
│   │   ├── histogram_plotter.py
│   ├── jobs/                 
│   │   ├── __init__.py
│   │   ├── job_fetcher.py
│   ├── misc/                 
│   │   ├── __init__.py
│   │   ├── motivation.py
│   ├── utils/                
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   ├── job_fields.py
│   │   ├── us_states.py
├── deploy/                   
│   ├── digitalocean.md
├── .env                      
├── .gitignore                
├── job_bot.py                
├── README.md                 
├── requirements.txt          
```

---

## Customization

### Adding More Job Fields

You can easily add more job fields by editing the `cogs/job_fields.py` file:

```python
from discord import app_commands

JOB_FIELDS = [
    app_commands.Choice(name='Computer Science', value='computer_science'),
    app_commands.Choice(name='Biology', value='biology'),
    app_commands.Choice(name='Engineering', value='engineering'),  # Example of adding a new field
    # Add more fields as needed
]
```

### Changing Auto Post Job Locations

To modify the states or fields for which jobs are automatically posted, update the `post_jobs()` function in `bot.py`:

```python
@tasks.loop(hours=6)
async def post_jobs():
    # Example: Automatically post Computer Science jobs in California
    cs_jobs = fetch_adzuna_jobs('computer science internship', location='California')
    
    # Example: Automatically post Biology jobs in New York
    bio_jobs = fetch_adzuna_jobs('biology internship', location='New York')
    
    # Customize job posting
    if cs_jobs:
        await channel.send("**Latest Computer Science Internships in California:**")
        job_listings_cs = format_jobs(cs_jobs)
        chunks_cs = split_message(job_listings_cs)
        for chunk in chunks_cs:
            await channel.send(chunk)
    
    if bio_jobs:
        await channel.send("**Latest Biology Internships in New York:**")
        job_listings_bio = format_jobs(bio_jobs)
        chunks_bio = split_message(job_listings_bio)
        for chunk in chunks_bio:
            await channel.send(chunk)           
```



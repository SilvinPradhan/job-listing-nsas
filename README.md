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

- **Fetch job listings**: Allows users to search for internships in specific fields and US states.
- **Scheduled job postings**: Automatically posts the latest job listings for predefined fields and locations at regular intervals (every 6 hours).
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

### `/job` Command

**Description**: Fetches the latest internship listings for a specific field in a US state.

**Usage**: `/job field:<job_field> state:<state_code>`

- **Field**: You can select between two job fields (`Computer Science` and `Biology`).
- **State**: You can enter a valid two-letter US state code (e.g., `CA` for California, `LA` for Louisiana, etc.).

**Example**: `/job field:Computer Science state:LA`

This command fetches the latest computer science internships available in Louisiana. The bot will format the response and return job titles, company names, locations, and links to apply.


If there are too many job listings, the bot will split the message into multiple chunks to stay within Discord's 2000-character message limit.

**Rate Limit**: The command is rate-limited to one request per 30 seconds per user to avoid overloading the API.

### Automatic Job Postings

The bot is configured to automatically post job listings to a specified Discord channel every 6 hours. The default setup fetches internships for predefined job fields and locations.

- **Computer Science** internships are posted in Louisiana.
- **Biology** internships are posted in Louisiana.

**Customizing Auto Postings**:
You can modify the code in the `post_jobs()` function (found in `bot.py`) to change the job fields and locations for automatic postings.

---

## File Structure

```plaintext
discord-bot/
├── bot.py                # Main bot file
├── .env                  # Environment variables (not pushed to GitHub)
├── .gitignore            # Git ignore file
├── requirements.txt      # Python dependencies
├── README.md             # Project description and instructions
├── cogs/                 # Folder to hold all separated functionalities (modules)
│   ├── __init__.py       # Marks directory as a package
│   ├── job_fetcher.py    # File containing job-fetching functions
│   ├── helpers.py        # Utility/helper functions for message splitting
│   ├── us_states.py      # Contains US state abbreviations and full names
│   ├── job_fields.py     # Contains job field choices
└── deploy/               # Deployment-related files
    └── digitalocean.md   # DigitalOcean deployment instructions
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



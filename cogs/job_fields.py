from discord import app_commands

# Define choices for job field (computer science and biology)
JOB_FIELDS = [
    app_commands.Choice(name='Computer Science', value='computer_science'),
    app_commands.Choice(name='Biology', value='biology')
]
from discord import app_commands

# Define choices for job fields, expanding to include more fields
JOB_FIELDS = [
    app_commands.Choice(name='Computer Science', value='computer_science'),
    app_commands.Choice(name='Biology', value='biology'),
    app_commands.Choice(name='Engineering', value='engineering'),
    app_commands.Choice(name='Marketing', value='marketing'),
    app_commands.Choice(name='Finance', value='finance'),
    app_commands.Choice(name='Design', value='design'),
    app_commands.Choice(name='Human Resources', value='human_resources'),
    app_commands.Choice(name='Sales', value='sales'),
    app_commands.Choice(name='Healthcare', value='healthcare'),
    app_commands.Choice(name='Education', value='education'),
    app_commands.Choice(name='Customer Service', value='customer_service'),
    app_commands.Choice(name='Project Management', value='project_management'),
    app_commands.Choice(name='Data Science', value='data_science'),
    app_commands.Choice(name='Accounting', value='accounting'),
    app_commands.Choice(name='Law', value='law'),
    app_commands.Choice(name='Construction', value='construction')
]

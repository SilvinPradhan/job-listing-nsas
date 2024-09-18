# Potential Enhancements

A Discord bot that helps users search and export job listings using the Adzuna API. Users can search for jobs using various parameters like custom keywords, company-specific searches, salary range, and even generate reports in Excel format.

## Features

### 1. Job Search by Custom Keywords [✅Task completed]
Search for jobs using any custom keywords for a more flexible job search. This allows users to specify exactly what they are looking for without being limited to predefined categories.

**Command**:  
`/search_jobs [keywords] [location]`

**Example**:  
`/search_jobs software engineer New York`

This command returns a list of job postings that match the provided keywords in the specified location.

---

### 2. Company-Specific Job Search
Users can search for job openings from specific companies, helping them target opportunities at companies they are most interested in.

**Command**:  
`/company_jobs [company_name] [location]`

**Example**:  
`/company_jobs Google California`

This command returns a list of job postings from the specified company in the provided location.

---

### 3. Job Posting by Salary Range
Filter job postings based on salary to focus on opportunities that match your compensation expectations. You can specify a minimum and maximum salary to fine-tune your search.

**Command**:  
`/search_by_salary [min_salary] [max_salary]`

**Example**:  
`/search_by_salary 50000 100000`

This command returns job listings with salaries that fall within the specified range.

---

### 4. Report Generation in Excel
Generate a detailed report of job postings for a specific field and location. The report will be created in an Excel file and can be downloaded with all relevant job details like job title, company, location, type, and salary.

**Command**:  
`/generate_report [job_field] [location]`

**Example**:  
`/generate_report computer_science Texas`

This command fetches the latest job listings for the specified job field and location, and generates an Excel report with the job data.

---

### 5. Daily Motivation Quote [🚧 Work in progress]
Automatically send a motivational quote to a designated channel at 8 AM every day using the [ZenQuotes API](https://zenquotes.io/). This feature is designed to help users start their day with a positive and inspiring message.

**Scheduled Task**:  
A daily task will trigger at 8 AM, posting a quote in a specified channel.

**Example**:  
_"Success is not final, failure is not fatal: It is the courage to continue that counts." – Winston Churchill_

This feature is currently being developed and will allow users to receive a motivational quote at the start of each day.

---

These features are designed to enhance your job search experience by providing flexible search options and the ability to export job data for easy access.

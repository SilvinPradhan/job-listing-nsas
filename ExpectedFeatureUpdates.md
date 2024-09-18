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

These features are designed to enhance your job search experience by providing flexible search options and the ability to export job data for easy access.

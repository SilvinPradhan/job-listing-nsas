import pandas as pd
from io import BytesIO
from datetime import datetime
from cogs.excel.excel_formatting import format_headers, format_salary_columns, set_column_widths

# Function to create an Excel file from the job data
def create_excel_file(jobs_data):
    job_list = []
    for job in jobs_data:
        created_date = job.get('created', None)
        if created_date:
            try:
                # "MM DD, YYYY"
                created_date = datetime.strptime(created_date, '%Y-%m-%dT%H:%M:%SZ').strftime('%m %d, %Y')
            except ValueError:
                created_date = 'Invalid Date'
        else:
            created_date = 'N/A'
        
        job_list.append({
            'Job Title': job.get('title', 'N/A'),
            'Company': job['company'].get('display_name', 'N/A'),
            'Location': job['location'].get('display_name', 'N/A'),
            'Salary Min': job.get('salary_min', 'N/A'),
            'Salary Max': job.get('salary_max', 'N/A'),
            'Contract Type': job.get('contract_type', 'N/A'),
            'Posted On': created_date,
            'Job URL': job.get('redirect_url', 'N/A')
        })
    
    df = pd.DataFrame(job_list)

    # Export DF to BytesIO stream as an Excel file
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Jobs', index=False)
    
    # Access xlsxwriter workbook and worksheet objs
    workbook  = writer.book
    worksheet = writer.sheets['Jobs']
    
    # Apply custom formatting
    format_headers(worksheet, df, workbook)
    format_salary_columns(worksheet, workbook)
    set_column_widths(worksheet)
    
    writer.close()
    output.seek(0)

    return output
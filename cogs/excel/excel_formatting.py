def format_headers(worksheet, df, workbook):
    bold_format = workbook.add_format({'bold': True})
    
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, bold_format)


def format_salary_columns(worksheet, workbook):
    dollar_format = workbook.add_format({'num_format': '"$"#,##0'})
    
    worksheet.set_column('D:D', 15, dollar_format)
    worksheet.set_column('E:E', 15, dollar_format)


def set_column_widths(worksheet):
    worksheet.set_column('A:A', 30)  # Job Title column width
    worksheet.set_column('B:B', 25)  # Company column width
    worksheet.set_column('C:C', 20)  # Location column width
    worksheet.set_column('F:F', 15)  # Contract Type column width
    worksheet.set_column('G:G', 20)  # Posted On column width
    worksheet.set_column('H:H', 40)  # Job URL column width
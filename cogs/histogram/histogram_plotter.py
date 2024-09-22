import matplotlib.pyplot as plt
from io import BytesIO

def plot_salary_histogram(histogram_data):
    try:
        # Prepare data for the histogram
        salary_ranges = sorted([int(salary) for salary in histogram_data if salary.isdigit()])
        vacancies = [int(histogram_data[salary]) for salary in map(str, salary_ranges)]  # Make sure salary is treated as string when accessing the dict

        if not salary_ranges or not vacancies:
            print("Error: No valid salary data to plot.")
            return None

        plt.figure(figsize=(8, 6))
        plt.bar(salary_ranges, vacancies, width=5000, color='blue')
        plt.xlabel('Salary ($)')
        plt.ylabel('Number of Vacancies')
        plt.title('Salary Distribution')

        # Save the plot to a buffer
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return buf

    except Exception as e:
        print(f"Error generating the histogram: {e}")
        return None

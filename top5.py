import pandas as pd

# Load the CSV file
file_path = 'TypeMetrics.csv'
data = pd.read_csv(file_path)

# Sort the data by LCOM4 in descending order and select the top 5 rows
top5_lcom4 = data.nlargest(5, 'LCOM4')

# Print the top 5 rows
print(top5_lcom4)

# Save the top 5 rows to a new CSV file
output_path = '/Users/banavathdirajnaik/lab_9/commons-cli/lcom_output/top5_lcom4.csv'
top5_lcom4.to_csv(output_path, index=False)
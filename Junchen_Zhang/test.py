import pandas as pd

# Load the dataset
file_path = r"D:\PostGrduate\MINI\rfm_data.csv"
rfm_data = pd.read_csv(file_path)

# Display the first few rows and describe the dataset to understand its structure
rfm_data_head = rfm_data.head()
rfm_data_description = rfm_data.describe()

print(rfm_data_head)
print(rfm_data_description)
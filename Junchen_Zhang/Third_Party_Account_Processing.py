import pandas as pd

uploaded_file_path = r"D:\PostGrduate\MINI\simulated_transaction_2024_Third_Party_Account.csv"
uploaded_data = pd.read_csv(uploaded_file_path)
#print(uploaded_data.head())

missing_values_uploaded = uploaded_data.isnull().sum()
#print(missing_values_uploaded)

# Remove rows where 'Balance' or 'Amount' is missing
uploaded_data_cleaned = uploaded_data.dropna(subset=['Balance', 'Amount'])

# Check the number of remaining records and show the first few rows to verify
remaining_records_cleaned = uploaded_data_cleaned.shape[0]
uploaded_data_cleaned.head(), remaining_records_cleaned

# Save the cleaned data back to the original file path
updated_file_path = r"D:\PostGrduate\MINI\simulated_transaction_2024_Third_Party_Account.csv"
uploaded_data_cleaned.to_csv(updated_file_path, index=False)

#print(missing_values_uploaded)
# Output the path to confirm the update
updated_file_path
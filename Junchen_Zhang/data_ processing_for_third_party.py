import pandas as pd

# Load the dataset to see the first few rows and understand its structure
file_path = r"D:\PostGrduate\MINI\simulated_transaction_2024.csv"
data = pd.read_csv(file_path)

# Correct understanding: remove rows where 'Account No' is missing
data_final_corrected = data.dropna(subset=['Account No'])

# Check the number of missing values after final cleaning and show the first few rows to verify
corrected_missing_values = data_final_corrected.isnull().sum()
corrected_missing_values, data_final_corrected.head()

# Remove rows where both 'Third Party Account No' and 'Third Party Name' are missing simultaneously
data_final_fully_cleaned = data_final_corrected.dropna(subset=['Third Party Account No', 'Third Party Name'], how='all')

# Check the number of missing values after this final cleaning and show the first few rows to verify
fully_cleaned_missing_values = data_final_fully_cleaned.isnull().sum()
fully_cleaned_missing_values, data_final_fully_cleaned.head()

# Fill missing values in 'Date' and 'Timestamp' using forward fill method
data_final_fully_cleaned['Date'] = data_final_fully_cleaned['Date'].fillna(method='ffill')
data_final_fully_cleaned['Timestamp'] = data_final_fully_cleaned['Timestamp'].fillna(method='ffill')

# Create a new dataframe containing only entries with a non-missing 'Third Party Account No'
data_with_third_party = data_final_fully_cleaned.dropna(subset=['Third Party Account No'])

# Select only specified columns for the new dataframe
data_with_third_party_filtered = data_with_third_party[['Date', 'Timestamp', 'Account No', 'Balance', 'Amount', 'Third Party Account No']]

output_file_path = r"D:\PostGrduate\MINI\simulated_transaction_2024_Third_Party_Account.csv"
data_with_third_party_filtered.to_csv(output_file_path, index=False)
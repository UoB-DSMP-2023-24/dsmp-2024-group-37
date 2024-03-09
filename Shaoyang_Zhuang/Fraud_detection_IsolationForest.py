import pandas as pd
import os
from sklearn.ensemble import IsolationForest

folder_path = 'zsy_expense_user'
files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

for file in files:
    data_path = os.path.join(folder_path, file)
    data = pd.read_csv(data_path)

    if data.empty or 'monopoly_money_amount' not in data.columns:
        print(f"Skipping file {data_path} as it is empty or lacks the required column.")
        continue

    # 检查列是否只有NaN值
    if data['monopoly_money_amount'].isna().all():
        print(f"Skipping file {data_path} as monopoly_money_amount column only contains NaN.")
        continue

    iso_forest = IsolationForest(n_estimators=200, contamination='auto', random_state=42)
    data['Isolation_Forest'] = iso_forest.fit_predict(data[['monopoly_money_amount']])
    data.to_csv(data_path, index=False)
    print(f"Modified file saved to {data_path}")

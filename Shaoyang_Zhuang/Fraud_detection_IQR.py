import pandas as pd
import os

# 定义文件夹路径
folder_path = 'zsy_expense_user'  # 根据实际情况调整路径

# 获取所有以".csv"结尾的文件
files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

for file in files:
    # 加载数据
    data_path = os.path.join(folder_path, file)
    data = pd.read_csv(data_path)

    # 计算IQR
    Q1 = data['monopoly_money_amount'].quantile(0.25)
    Q3 = data['monopoly_money_amount'].quantile(0.75)
    IQR = Q3 - Q1

    # 标记异常值和正常值
    data['IQR'] = data['monopoly_money_amount'].apply(
        lambda x: -1 if x < (Q1 - 1.5 * IQR) or x > (Q3 + 1.5 * IQR) else 1)

    # 保存修改后的数据到CSV文件，直接覆盖原文件
    data.to_csv(data_path, index=False)

    print(f"Modified file saved to {data_path}")

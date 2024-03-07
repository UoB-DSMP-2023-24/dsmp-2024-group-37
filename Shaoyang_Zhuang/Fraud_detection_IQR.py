import pandas as pd
import os

# 定义文件夹路径
folder_path = 'tj'  # 根据实际情况调整路径

# 定义输出文件的路径（保存在当前工作目录）
result_file = 'outlier_IQR.csv'  # 输出文件将直接保存在当前工作目录

# 获取所有以"group_"开头的.csv文件
files = [f for f in os.listdir(folder_path) if f.startswith('group_') and f.endswith('.csv')]

# 准备一个空的DataFrame来收集所有异常值行
all_outliers = pd.DataFrame()

for file in files:
    # 加载数据
    data_path = os.path.join(folder_path, file)
    data = pd.read_csv(data_path)

    # 计算IQR和异常值边界
    Q1 = data['monopoly_money_amount'].quantile(0.25)
    Q3 = data['monopoly_money_amount'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # 识别异常值
    outliers = data[(data['monopoly_money_amount'] < lower_bound) | (data['monopoly_money_amount'] > upper_bound)]

    # 如果存在异常值，则添加到all_outliers DataFrame中
    if not outliers.empty:
        all_outliers = pd.concat([all_outliers, outliers], ignore_index=True)

# 将所有异常值行输出到一个新的CSV文件
all_outliers.to_csv(result_file, index=False)

# 输出结果文件的路径，以便于下载或进一步处理
print(f"Outliers saved to {result_file}")

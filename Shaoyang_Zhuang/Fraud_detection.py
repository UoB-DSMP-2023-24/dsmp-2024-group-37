import os
import pandas as pd

# 文件夹路径
folder_path = 'zsy_expense_user'

# 新建一个DataFrame，用来存储所有文件的统计结果
fraud_detection_df = pd.DataFrame(
    columns=['from_totally_fake_account', 'Z-score_count', 'IQR_count', 'Isolation_Forest_count'])

# 遍历文件夹内的所有.csv文件
for file in os.listdir(folder_path):
    if file.endswith('.csv'):
        # 获取用户号
        user_account = file.split('_')[1].split('.')[0]

        # 读取CSV文件
        file_path = os.path.join(folder_path, file)
        data = pd.read_csv(file_path)

        # 如果文件中没有数据，设置计数为0
        if data.empty:
            z_score_count = 0
            iqr_count = 0
            isolation_forest_count = 0
        else:
            # 计算Z-score, IQR, 和Isolation_Forest中值为-1的数量
            z_score_count = (data['Z-score'] == -1).sum()
            iqr_count = (data['IQR'] == -1).sum()
            isolation_forest_count = (data['Isolation_Forest'] == -1).sum()

        # 将统计结果添加到fraud_detection_df中
        fraud_detection_df = fraud_detection_df.append({'from_totally_fake_account': user_account,
                                                        'Z-score_count': z_score_count,
                                                        'IQR_count': iqr_count,
                                                        'Isolation_Forest_count': isolation_forest_count},
                                                       ignore_index=True)

# 保存结果到Fraud_detection.csv文件
fraud_detection_df.to_csv('Fraud_detection.csv', index=False)

print("处理完成，结果已保存到Fraud_detection.csv文件中。")

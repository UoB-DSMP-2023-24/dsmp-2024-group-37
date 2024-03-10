# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 08:29:23 2024

@author: T
"""
import glob
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

#读取数据
#data = pd.read_csv("D:/MiniProjectSource/dsmp-2024-group-37/JIA_TIAN/fake_transactional_data_24.csv")
#data = pd.read_csv("D:/MiniProjectSource/dsmp-2024-group-37/JIA_TIAN/DataTransfer.csv")

#合并数据
#path = 'D:/MiniProjectSource/CoffeeRFM'
#csv = glob.glob(f"{path}/*.csv")
#df_list = []
#for file in csv:
#    df = pd.read_csv(file)
#    df_list.append(df)
#merge = pd.concat(df_list, axis=0)
#merge = merge.reset_index(drop=True)
#merge.to_csv('D:/MiniProjectSource/CoffeeRFM/merge.csv', index=False)


# 假设文件名为 'example.csv'，你可以根据实际情况修改
path = 'D:/MiniProjectSource/CoffeeRFM'
csv = glob.glob(f"{path}/*.csv")
df_list = []
for file in csv:
    df = pd.read_csv(file)
    # 获取不包含路径和扩展名的纯文件名
    base_name = file.split('.')[0]
    df['merchant'] = base_name
    df_list.append(df)
merge = pd.concat(df_list, axis=0)
merge = merge.reset_index(drop=True)
merge.to_csv('D:/MiniProjectSource/CoffeeRFM/CoffeeMerge.csv', index=False)

# 如果你的文件名中包含路径，可以使用os.path.split()和os.path.splitext()组合来获取




#RFM打分
#def assign_score(value, breakpoints, scores):
#    """根据断点分配分数"""
#    for i, point in enumerate(breakpoints):
#        if value <= point:
#            return scores[i]
#    return scores[-1]
#
#path = 'D:/MiniProjectSource/Coffee'
#csv = glob.glob(f"{path}/*.csv")
#for file in csv:
#    df = pd.read_csv(file)
## Monetary 和 Frequency 打分
#    for col in ['Monetary', 'Frequency']:
#        # 计算每20%的分位数
#        breakpoints = np.percentile(df[col], [20, 40, 60, 80])
#        # 分配分数，分数越高代表值越大
#        
#        scores = [1, 2, 3, 4, 5]
#        df[f'{col}_score'] = df[col].apply(assign_score, args=(breakpoints, scores))
#
## Recency 打分，逻辑相反，值越小分数越高
#    breakpoints = np.percentile(df['Recency'], [20, 40, 60, 80])
#    scores = [5, 4, 3, 2, 1]  # Recency 的分数分配逻辑与 Monetary 和 Frequency 相反
#    df['Recency_score'] = df['Recency'].apply(assign_score, args=(breakpoints, scores))
#    df = df.reset_index(drop=True)
#    df.to_csv(file, index=False)
    
#RFM分级
# 定义一个函数，根据M、F、R与它们的平均值的比较，生成标记
#def assign_grade(row):
#    r_grade = '1' if row['Recency'] < average_R else '0'
#    f_grade = '1' if row['Frequency'] > average_F else '0'
#    m_grade = '1' if row['Monetary'] > average_M else '0'
#    return f"{r_grade}{f_grade}{m_grade}"  # 直接格式化为三个字符的字符串
#   
#path = 'D:/MiniProjectSource/CoffeeRFM'
#csv = glob.glob(f"{path}/*.csv")
#for file in csv:
#    df = pd.read_csv(file)
## 计算平均值
#    average_M = df['Monetary'].mean()
#    average_F = df['Frequency'].mean()
#    average_R = df['Recency'].mean()
#
## 应用这个函数到每一行
#    df['grade'] = df.apply(assign_grade, axis=1)
#    df = df.reset_index(drop=True)
#    df.to_csv(file, index=False)

# 假设你的DataFrame名为df，且你想将列名为'your_column_name'的列转换为字符串类型
#print(data1.dtypes)
#data['from_totally_fake_account'] = data['from_totally_fake_account'].astype(int)
#data['from_totally_fake_account'] = data['from_totally_fake_account'].astype(str)
#data['not_happened_yet_date'] = pd.to_datetime(data['not_happened_yet_date'], format='%d/%m/%Y')
#
##data['to_randomly_generated_account'] = data['to_randomly_generated_account'].astype(str)
#data.to_csv("D:/MiniProjectSource/dsmp-2024-group-37/JIA_TIAN/DataTransfer.csv", index=False)

# 1分组键
#group_keys = ['from_totally_fake_account', 'to_randomly_generated_account'] 
#
#for key in group_keys:
#    # 对每个键进行分组
#    grouped = data.groupby(key)
#    for name, group in grouped:
#        if type(name) == str:
#            filename = f"D:/MiniProjectSource/JIA_TIAN/group_{name}.csv"
#        else:
#        # 确保文件名是合法的，例如去除特殊字符等，这里简化处理，直接将其转为字符串
#            filename = f"D:/MiniProjectSource/JIA_TIAN/group_{str(int(name))}.csv"
#        
#        # 检查文件是否存在
#        if os.path.exists(filename):
#            # 如果文件存在，追加模式写入，不包括表头
#            group.to_csv(filename, mode='a', header=False, index=False)
#        else:
#            # 如果文件不存在，正常写入，包括表头
#            group.to_csv(filename, index=False)

#group_keys = ['to_randomly_generated_account'] 
#
#for key in group_keys:
#    # 对每个键进行分组
#    grouped = data.groupby(key)
#    for name, group in grouped:
#        if type(name) == str:
#            filename = f"D:/MiniProjectSource/group_{name}.csv"
#            # 如果文件不存在，正常写入，包括表头
#            group.to_csv(filename, index=False)


# 2判断某一列是否有空值
#column_name = 'monopoly_money_amount'
#if data[column_name].isnull().values.any():
#    print(f"列 '{column_name}' 中存在空值")
#else:
#    print(f"列 '{column_name}' 中不存在空值")


#3根据from_totally_fake_account分组并计算开销和
#group_from = data.groupby('from_totally_fake_account')['monopoly_money_amount'].sum().rename('total_amount').reset_index()
#group_from.to_csv('D:/MiniProjectSource/GroupFrom.csv', index=False)

#4根据to_randomly_generated_account分组并计算收入和
#group_to = data.groupby('to_randomly_generated_account')['monopoly_money_amount'].sum().rename('total_amount').reset_index()
#group_to.to_csv('D:/MiniProjectSource/GroupTo.csv', index=False)


        
#folder_path = 'D:/MiniProjectSource'
#
#for filename in os.listdir(folder_path):
#    file_path = os.path.join(folder_path, filename)
#    # 确保是文件而不是文件夹
#    if os.path.isfile(file_path):
#        # 读取文件
#        df = pd.read_csv(file_path)
#        df['not_happened_yet_date'] = pd.to_datetime(df['not_happened_yet_date'], format='%d/%m/%Y')
#        
#        # 获取数据集的最新日期作为"今天"的日期，用于计算Recency
#        today = df['not_happened_yet_date'].max()
#        
#        # 按照from_totally_fake_account列分组
#        grouped = df.groupby('from_totally_fake_account')
#        
#        # 对每个分组计算monopoly_money_amount列的和以及频率（数据条数）
#        monetary_frequency = grouped['monopoly_money_amount'].agg(['sum', 'count']).reset_index()
#        monetary_frequency.columns = ['from_totally_fake_account', 'Monetary', 'Frequency']  # 重命名列以匹配您的要求
#        # 计算每个用户的最近交易日期与今天日期的差值，得到Recency
#        recency = grouped['not_happened_yet_date'].max().reset_index()
#        recency['Recency'] = (today - recency['not_happened_yet_date']).dt.days
#        recency = recency[['from_totally_fake_account', 'Recency']]
#        
#        # 合并结果以创建最终的DataFrame
#        result = pd.merge(monetary_frequency, recency, on='from_totally_fake_account', how='inner')
#        
#        # 将修改后的DataFrame写回文件，替换原文件
#        result.to_csv(file_path, index=False)

# 5对'monopoly_money_amount'进行求和
#sum_df = data.groupby(['from_totally_fake_account', 'to_randomly_generated_account'])['monopoly_money_amount'].sum().rename('total_amount').reset_index()
#
## 计算'to_randomly_generated_account'的出现频次
#count_df = data.groupby(['from_totally_fake_account', 'to_randomly_generated_account']).size().rename('frequency').reset_index()
#
### 合并两个结果
#merged = pd.merge(sum_df, count_df, on=['from_totally_fake_account', 'to_randomly_generated_account'])
#merged.to_csv('D:/MiniProjectSource/GroupFromTo.csv', index=False)

#6
#merged = pd.read_csv("D:/MiniProjectSource/JIA_TIAN/GroupFromTo.csv")
## 筛选出纯数字的行，即普通客户
#customers_df = merged[merged['to_randomly_generated_account'].apply(lambda x: x.isnumeric())]
#
## 筛选出纯字母的行，即商家
#merchants_df = data[~data['to_randomly_generated_account'].apply(lambda x: x.isnumeric())]
#
## 重置索引
#customers_df_sorted = customers_df.reset_index(drop=True)
#merchants_df_sorted = merchants_df.reset_index(drop=True)

## 7对customers_df按照from_totally_generated_account进行分组
#customers_grouped = customers_df_sorted.groupby('from_totally_fake_account')
#
## 遍历每个分组，并将每个分组保存为CSV文件
#for account, group in customers_grouped:
#    filename = f"D:/MiniProjectSource/JIA_TIAN/customers_group_{account}.csv"
#    group.to_csv(filename, index=False)
    
## 对merchants_df按照from_totally_generated_account进行分组
#merchants_grouped = merchants_df_sorted.groupby('from_totally_fake_account')
#
## 遍历每个分组，并将每个分组保存为CSV文件
#for account, group in merchants_grouped:
#    filename = f"D:/MiniProjectSource/JIA_TIAN/merchants_group_{account}.csv"
#    group.to_csv(filename, index=False)


## 保存排序后的DataFrame为CSV文件
#customers_df_sorted.to_csv('D:/MiniProjectSource/JIA_TIAN/customers_sorted.csv', index=False)
#merchants_df_sorted.to_csv('D:/MiniProjectSource/merchants.csv', index=False)


import pandas as pd
from datetime import datetime

# scan CSV document
df = pd.read_csv(r"D:\PostGrduate\MINI\LloydsBank_FakeData.csv")

# 数据预览
#df_head = df.head()
#df_info = df.info()

#print(df_head)
#print(df_info)

# 转换日期格式
df['not_happened_yet_date'] = pd.to_datetime(df['not_happened_yet_date'], format='%d/%m/%Y', errors='coerce')

# 检查并移除金额为负和为0的记录
df = df[df['monopoly_money_amount'] > 0]

# 再次检查数据信息以确认转换成功和数据清洗的结果
#df_info_after_cleaning = df.info()
#df_head_after_cleaning = df.head()

#print(df_head_after_cleaning)
#print(df_info_after_cleaning)

#计算R值
#对每个to_randomly_generated_account，按not_happened_yet_date降序排列数据。
#计算相邻两次消费的时间差。
# 假设当前日期为数据集中的最大日期
current_date = df['not_happened_yet_date'].max()

# 计算每个账户的最近一次消费日期和上一次消费日期
df_sorted = df.sort_values(by=['to_randomly_generated_account', 'not_happened_yet_date'], ascending=[True, False])
df_sorted['previous_transaction_date'] = df_sorted.groupby('to_randomly_generated_account')['not_happened_yet_date'].shift(-1)

# 计算Recency（最近一次消费和上一次消费的时间间隔）
df_sorted['recency'] = (df_sorted['not_happened_yet_date'] - df_sorted['previous_transaction_date']).dt.days

# 预览计算结果
df_recency_preview = df_sorted[['to_randomly_generated_account', 'not_happened_yet_date', 'previous_transaction_date', 'recency']].head()

#print(df_recency_preview)

#Frequency (F值) 将基于在数据集最大日期往前一年内的消费次数来计算。
#Monetary (M值) 将计算在同一时间期限内的总消费金额。
# 计算过去一年的日期范围
one_year_ago = current_date - pd.DateOffset(years=1)

# 筛选过去一年内的数据
df_one_year = df_sorted[df_sorted['not_happened_yet_date'] > one_year_ago]

# 计算Frequency（F值）：过去一年内每个账户的消费次数
df_frequency = df_one_year.groupby('to_randomly_generated_account').size().reset_index(name='frequency')

# 计算Monetary（M值）：过去一年内每个账户的总消费金额
df_monetary = df_one_year.groupby('to_randomly_generated_account')['monopoly_money_amount'].sum().reset_index(name='monetary')

# 预览F值和M值的计算结果
df_frequency_preview = df_frequency.head()
df_monetary_preview = df_monetary.head()

# 将F值和M值合并到一个DataFrame中
df_rf = pd.merge(df_frequency, df_monetary, on='to_randomly_generated_account', how='outer')

# 从df_sorted中提取每个账户的最新Recency值（考虑到只计算最近一次和上一次消费的间隔）
df_recency = df_sorted.drop_duplicates(subset=['to_randomly_generated_account'], keep='first')[['to_randomly_generated_account', 'recency']]

# 将R值合并到RF值DataFrame中
df_rfm = pd.merge(df_rf, df_recency, on='to_randomly_generated_account', how='outer')

print(df_rfm)

# 将最终的RFM结果保存到CSV文件中
output_file_path = 'D:\PostGrduate\MINI\RFM_Analysis.csv'
df_rfm.to_csv(output_file_path, index=False)

print(output_file_path)
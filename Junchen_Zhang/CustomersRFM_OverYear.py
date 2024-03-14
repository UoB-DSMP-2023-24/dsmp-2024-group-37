import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


pd.set_option('display.max_columns', None)

# scan CSV document
df = pd.read_csv(r"D:\PostGrduate\MINI\fake_transactional_data_24.csv")

# Convert 'not_happened_yet_date' to datetime format
df['not_happened_yet_date'] = pd.to_datetime(df['not_happened_yet_date'], format='%d/%m/%Y', errors='coerce')

# Get the maximum date in the dataset to find out the last transaction date
max_date = df['not_happened_yet_date'].max()

# Define one year ago from the last transaction date for filtering
one_year_ago = max_date - pd.DateOffset(years=1)

# Filter transactions that occurred in the last year
df_last_year = df[df['not_happened_yet_date'] > one_year_ago]

# Calculate Monetary (M): Total money spent by each account over the past year
monetary = df_last_year.groupby('from_totally_fake_account')['monopoly_money_amount'].sum().reset_index(name='monetary')

# Calculate Frequency (F): Total number of transactions by each account over the past year
frequency = df_last_year.groupby('from_totally_fake_account').size().reset_index(name='frequency')

rfm_table = monetary.merge(frequency, on='from_totally_fake_account')

# For Recency (R), we need to calculate the days between the last transaction and the second last transaction
# Sort transactions for each account by date
df_last_year_sorted = df_last_year.sort_values(by=['from_totally_fake_account', 'not_happened_yet_date'], ascending=[True, False])

# 按账户分组并获取每个账户最近的交易日期
most_recent_purchase = df_last_year.groupby('from_totally_fake_account')['not_happened_yet_date'].max().reset_index()

# 计算最近一次购买到数据集中最新日期的天数差
most_recent_purchase['recency'] = (max_date - most_recent_purchase['not_happened_yet_date']).dt.days

# 然后合并新计算的R值
rfm_table= rfm_table.merge(most_recent_purchase[['from_totally_fake_account', 'recency']], on='from_totally_fake_account', how='left')
# Calculate the average values for R, F, and M
rfm_averages = rfm_table[['recency', 'frequency', 'monetary']].mean()

# Define the path where the CSV file will be saved
output_csv_path = r"D:\PostGrduate\MINI\CustomersRFM_OverYear_analysis.csv"

# Save the updated dataframe to a CSV file
rfm_table.to_csv(output_csv_path, index=False)

# 计算Recency分布
recency_counts = rfm_table['recency'].value_counts(normalize=True).sort_index() * 100

# 计算Frequency分布
frequency_counts = rfm_table['frequency'].value_counts(normalize=True).sort_index() * 100

# 计算Monetary分布
monetary_counts = rfm_table['monetary'].value_counts(normalize=True).sort_index() * 100

# 绘制Recency趋势图
plt.figure(figsize=(12, 6))
recency_counts.plot(kind='bar')
plt.title('Recency Distribution')
plt.xlabel('Days Since Last Purchase')
plt.ylabel('Percentage of Customers (%)')
plt.show()

# 绘制Recency分布的直方图
plt.figure(figsize=(12, 6))
sns.histplot(rfm_table['recency'], bins=30, kde=True)  # 使用Seaborn的histplot函数，同时绘制直方图和密度曲线
plt.title('Recency Distribution')
plt.xlabel('Days Since Last Purchase')
plt.ylabel('Number of Customers')
plt.show()

# 绘制Frequency趋势折线图
plt.figure(figsize=(12, 6))
frequency_counts.plot(kind='line', marker='o')  # 使用frequency_counts变量
plt.title('Frequency Distribution')
plt.xlabel('Number of Transactions')
plt.ylabel('Percentage of Customers (%)')
plt.grid(True)  # 添加网格线
plt.show()

# 计算Monetary分布
# 对Monetary的分布进行处理可能稍微复杂一些，因为Monetary值可能非常分散
# 这里假设我们直接用存在的Monetary值，但实际应用中可能需要按区间分组
monetary_counts = rfm_table.groupby('monetary').size() / len(rfm_table) * 100
monetary_counts = monetary_counts.sort_index()

# 绘制Monetary趋势折线图
plt.figure(figsize=(12, 6))
monetary_counts.plot(kind='line', marker='o') # 添加marker='o'以显示数据点
plt.title('Monetary Distribution')
plt.xlabel('Total Spent')
plt.ylabel('Percentage of Customers (%)')
plt.grid(True) # 添加网格线
plt.show()

# Recency得分：越近的得分越高
bins = [-1,0, 1, 2, 3, max(rfm_table['recency'])+1]
labels = [5, 4, 3, 2, 1]
rfm_table['R_score'] = pd.cut(rfm_table['recency'], bins=bins, labels=labels)

# Frequency得分：越频繁的得分越高
rfm_table['F_score'] = pd.qcut(rfm_table['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])

# Monetary得分：花费越多的得分越高
rfm_table['M_score'] = pd.qcut(rfm_table['monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])

# 计算R, F, M的平均值
R_average = rfm_table['recency'].mean()
F_average = rfm_table['frequency'].mean()
M_average = rfm_table['monetary'].mean()

rfm_table['R Compare'] = rfm_table['recency'].apply(lambda x: 'high' if x <= R_average else 'low')
rfm_table['F Compare'] = rfm_table['frequency'].apply(lambda x: 'high' if x >= F_average else 'low')
rfm_table['M Compare'] = rfm_table['monetary'].apply(lambda x: 'high' if x >= M_average else 'low')

def categorize_rfm(row):
    if row['R Compare'] == 'high' and row['F Compare'] == 'high' and row['M Compare'] == 'high':
        return'important value customers'
    elif row['R Compare'] == 'low' and row['F Compare'] == 'high' and row['M Compare'] == 'high':
        return'Important to keep customers'
    elif row['R Compare'] == 'high' and row['F Compare'] == 'low' and row['M Compare'] == 'high':
        return'Important development customers'
    elif row['R Compare'] == 'high' and row['F Compare'] == 'high' and row['M Compare'] == 'low':
        return'General value customers'
    elif row['R Compare'] == 'low' and row['F Compare'] == 'high' and row['M Compare'] == 'low':
        return'Generally keep customers'
    elif row['R Compare'] == 'high' and row['F Compare'] == 'low' and row['M Compare'] == 'low':
        return'General development users'
    elif row['R Compare'] == 'low' and row['F Compare'] == 'low' and row['M Compare'] == 'high':
        return'Important customer recall'
    elif row['R Compare'] == 'low' and row['F Compare'] == 'low' and row['M Compare'] == 'low':
        return'General recall of customers'
    # ... 为其他类别继续添加条件分支 ...
    else:
        return 'other'

# 应用函数分类到新列
rfm_table['Category'] = rfm_table.apply(categorize_rfm, axis=1)
# 统计每种类型的客户数量
customer_type_counts = rfm_table['Category'].value_counts(normalize=True)

# 排序并找出最小的三个类别
smallest_categories = customer_type_counts.nsmallest(1).index

# 将每个部分稍微分离出来，提供一个explode列表
explode = [0.05] * len(customer_type_counts)  # 为每个部分都设置稍微分离，确保没有重叠
# 定义环形图的中心空白参数
wedgeprops = {'width': 0.3, 'edgecolor': 'w'}  # 定义环形的宽度和边缘颜色

# 画饼状图，增加explode参数
# plt.figure(figsize=(10, 8))
# patches, texts, autotexts = plt.pie(customer_type_counts, autopct='%1.1f%%',
#                                     startangle=90, explode=explode, pctdistance=0.85)

# 调整autopct标签的位置，使其错开
# for i, autotext in enumerate(autotexts):
#     if customer_type_counts.index[i] in smallest_categories:  # 最小的三个类别
        # 获取百分比标签的位置
#        x, y = autotext.get_position()
        # 将标签移动到图表外部，使用annotate来添加指向饼图的线
#        plt.annotate(
#           autotext.get_text(), xy=(x, y), xytext=(1.5*x, 1.25*y),
#             arrowprops=dict(arrowstyle="-", color='grey'), ha='center',
#             fontsize=8
#        )
#        autotext.set_visible(False)  # 隐藏原autopct标签
# 添加图例
# plt.legend(patches, customer_type_counts.index, loc='upper left', bbox_to_anchor=(-0.1, 1.),
#           fontsize=8)

# plt.title('Proportion of each customer type')
# plt.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.
# plt.ylabel('')  # 隐藏y轴标签
# plt.show()
plt.figure(figsize=(10, 8))
patches, texts, autotexts = plt.pie(customer_type_counts, autopct='%1.1f%%',
                                    startangle=90, explode=explode,
                                    pctdistance=0.85, wedgeprops=wedgeprops)

# 调整autopct标签的位置，使其错开
for i, autotext in enumerate(autotexts):
    if customer_type_counts.index[i] in smallest_categories:  # 最小的三个类别
        x, y = autotext.get_position()
        plt.annotate(
            autotext.get_text(), xy=(x, y), xytext=(1.5*x, 1.25*y),
            arrowprops=dict(arrowstyle="-", color='grey'), ha='center',
            fontsize=8
        )
        autotext.set_visible(False)

# 添加图例
plt.legend(patches, customer_type_counts.index, loc='upper left', bbox_to_anchor=(-0.1, 1.),
           fontsize=8)

plt.title('Proportion of each customer type')
plt.axis('equal')  # 保证圆形
plt.ylabel('')

plt.show()
# 打印结果以及保存到CSV
print(rfm_table.head())
rfm_table.to_csv(output_csv_path, index=False)

# 将数据保存到CSV文件
output_csv_path = "CustomersRFM_OverYear_analysis.csv"
rfm_table.to_csv(output_csv_path, index=False)
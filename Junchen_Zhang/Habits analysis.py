import pandas as pd
# 可视化部分
import matplotlib.pyplot as plt

# 加载数据
data = pd.read_csv(r"D:\PostGrduate\MINI\simulated_transaction_2024_Third_Party_Account.csv")

# 转换日期格式
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')

# 计算每个账户每天的转账次数
daily_transfers = data.groupby(['Account No', 'Date']).size().groupby('Account No').mean()

# 计算每个账户的转账金额统计信息
amount_stats = data.groupby('Account No')['Amount'].describe()

# 输出结果
print("Number of transfers per day：", daily_transfers.head())
print("Transfer amount statistics：", amount_stats.head())

# 计算每日的总转账次数和总金额
daily_transactions = data.groupby(data['Date'].dt.date).agg(
    Transactions=('Account No', 'size'),  # 统计每日的交易次数
    Total_Amount=('Amount', 'sum')  # 统计每日的总金额
).reset_index()

# 绘制每日交易次数
plt.figure(figsize=(14, 7))
plt.plot(daily_transactions['Date'], daily_transactions['Transactions'], label='Daily Transactions')
plt.title('Daily Transactions Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Transactions')
plt.grid(True)
plt.legend()
plt.show()

# 绘制每日总金额
plt.figure(figsize=(14, 7))
plt.plot(daily_transactions['Date'], daily_transactions['Total_Amount'], color='red', label='Daily Total Amount')
plt.title('Daily Total Transaction Amount Over Time')
plt.xlabel('Date')
plt.ylabel('Total Amount')
plt.grid(True)
plt.legend()
plt.show()


# 提取每个客户每日、每周和每月的转账次数
data['Day'] = data['Date'].dt.day
data['Week'] = data['Date'].dt.isocalendar().week
data['Month'] = data['Date'].dt.month
data['Weekday'] = data['Date'].dt.weekday

# 转账频率分布
daily_frequency = data.groupby(['Account No', 'Day']).size().groupby('Account No').describe()
weekly_frequency =data.groupby(['Account No', 'Week']).size().groupby('Account No').describe()
monthly_frequency = data.groupby(['Account No', 'Month']).size().groupby('Account No').describe()

# 转账金额分布
amount_distribution = data.groupby('Account No')['Amount'].describe()

# 转账时间分布
weekday_distribution = data.groupby(['Account No', 'Weekday']).size().groupby('Account No').describe()

print(daily_frequency)
print(weekly_frequency)
print(monthly_frequency)
print(amount_distribution)


# 可视化转账金额的分布（直方图）
plt.figure(figsize=(10, 6))
amount_stats['mean'].hist(bins=20)
plt.title('Distribution of Average Transaction Amount')
plt.xlabel('Average Amount')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# 可视化转账次数的分布（箱形图）
plt.figure(figsize=(10, 6))
daily_frequency['mean'].plot(kind='box', vert=False)
plt.title('Distribution of Average Daily Transaction Frequency')
plt.xlabel('Average Daily Transactions')
plt.grid(True)
plt.show()
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
# 加载数据
df = pd.read_csv(r"D:\PostGrduate\MINI\CustomersRFM_OverYear_analysis.csv")

# 计算total_transactions和total_amount_spent
user_activity = df.groupby('from_totally_fake_account').agg(
    total_transactions=('frequency', 'sum'),
    total_amount_spent=('monetary', 'sum')
).reset_index()

# 使用qcut分档
user_activity['transactions_quintile'] = pd.qcut(user_activity['total_transactions'], 5, labels=[1, 2, 3, 4, 5])
user_activity['amount_quintile'] = pd.qcut(user_activity['total_amount_spent'], 5, labels=[1, 2, 3, 4, 5])

# 计算平均值
avg_transactions = user_activity['total_transactions'].mean()
avg_amount_spent = user_activity['total_amount_spent'].mean()

# 标记高/低活动度
user_activity['transactions_level'] = user_activity['total_transactions'].apply(lambda x: 'High' if x > avg_transactions else 'Low')
user_activity['amount_level'] = user_activity['total_amount_spent'].apply(lambda x: 'High' if x > avg_amount_spent else 'Low')

user_activity['activity_score'] = (user_activity['transactions_quintile'].astype(int) * 0.4) + (user_activity['amount_quintile'].astype(int) * 0.6)

# Sort users by their new weighted activity score
user_activity_sorted_by_weighted_score = user_activity.sort_values(by='activity_score', ascending=False)

most_active_users = user_activity_sorted_by_weighted_score.head(10)
least_active_users = user_activity_sorted_by_weighted_score.tail(10)

print("最活跃的用户：")
print(most_active_users[['from_totally_fake_account', 'activity_score', 'total_transactions', 'total_amount_spent']])
print("\n最不活跃的用户：")
print(least_active_users[['from_totally_fake_account', 'activity_score', 'total_transactions', 'total_amount_spent']])

# Sorting the user_activity DataFrame by 'activity_score' to prepare for CDF plot
user_activity_sorted_by_activity_score = user_activity.sort_values('activity_score')

# Generating the CDF of the activity scores
user_activity_sorted_by_activity_score['cdf'] = user_activity_sorted_by_activity_score['activity_score'].rank(method='average', pct=True)

# Plotting the CDF
plt.figure(figsize=(12, 7))
plt.plot(user_activity_sorted_by_activity_score['activity_score'], user_activity_sorted_by_activity_score['cdf'], marker='.', linestyle='none')
plt.title('Cumulative Distribution Function (CDF) of Activity Scores')
plt.xlabel('Activity Score')
plt.ylabel('CDF')
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.boxplot(user_activity_sorted_by_weighted_score['activity_score'], vert=False, patch_artist=True)
plt.title('Box Plot of Weighted Activity Scores')
plt.xlabel('Weighted Activity Score')
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# Histogram for weighted activity score
plt.figure(figsize=(10, 6))
plt.hist(user_activity_sorted_by_weighted_score['activity_score'], bins=20, color='skyblue', edgecolor='black')
plt.title('Histogram of Weighted Activity Scores')
plt.xlabel('Weighted Activity Score')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)
plt.show()

# Since Scatter Plot requires two variables, let's plot 'total_transactions' vs. 'total_amount_spent'
plt.figure(figsize=(10, 6))
plt.scatter(user_activity_sorted_by_weighted_score['total_transactions'], user_activity_sorted_by_weighted_score['total_amount_spent'], alpha=0.6, edgecolors='w', color='purple')
plt.title('Scatter Plot of Total Transactions vs. Total Amount Spent')
plt.xlabel('Total Transactions')
plt.ylabel('Total Amount Spent')
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# 将数据保存到CSV文件
output_csv_path = "Activity_Analysis.csv"
user_activity_sorted_by_weighted_score.to_csv(output_csv_path, index=False)
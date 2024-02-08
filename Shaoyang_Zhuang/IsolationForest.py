import pandas as pd
from sklearn.ensemble import IsolationForest

# 加载数据
df = pd.read_csv('dataset(new).csv')

# 尝试将account转换为数值类型，失败的（即字符串）标记为NaN
df['account_numeric'] = pd.to_numeric(df['account'], errors='coerce')

# 仅保留account转换成功的行，即去掉account为字符串的记录
df = df.dropna(subset=['account_numeric'])

# 选择模型使用的特征（不包括account）
features = ['transaction', 'income_count', 'expense_count']  # 根据实际情况调整
X = df[features]

# 初始化Isolation Forest模型，调整contamination参数
# 假设异常值比例大约为 121 / 22378，但我们会设置一个稍低的值以避免过多的误报
contamination_rate = 121 / 22378

clf = IsolationForest(n_estimators=100,
                      contamination=contamination_rate,
                      max_samples='auto',
                      random_state=42)

# 拟合模型
clf.fit(X)

# 预测：-1表示异常，1表示正常
df['anomaly'] = clf.predict(X)

# 计算异常值数量
num_anomalies = df['anomaly'].value_counts().get(-1, 0)
print(f"Number of anomalies detected: {num_anomalies}")

# 保存带有异常标记的数据集到新的CSV文件（包括原始account列）
df.to_csv('dataset_with_anomalies.csv', columns=['account'] + features + ['anomaly'], index=False)

import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 加载数据集
data = pd.read_csv(r"D:\PostGrduate\MINI\rfm_data.csv")

# 标准化整个数据集
scaler = StandardScaler()
rfm_features = ['R', 'F', 'M']
data[rfm_features] = scaler.fit_transform(data[rfm_features])

# 创建3D图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 应用DBSCAN算法
# 应用DBSCAN算法
dbscan = DBSCAN(eps=0.9, min_samples=2)
data['Cluster'] = dbscan.fit_predict(data[rfm_features])

# 为每个簇分配不同的颜色
colors = ['blue', 'orange']  # 假设我们有两个聚类和噪声

# 绘制所有点
for cluster in np.unique(data['Cluster']):
    cluster_data = data[data['Cluster'] == cluster]
    ax.scatter(cluster_data['R'], cluster_data['F'], cluster_data['M'],
               color=colors[cluster] if cluster != -1 else 'grey',  # 噪声用灰色表示
               label=f'Cluster {cluster}' if cluster != -1 else 'Noise', s=5)  # 调整点的大小为20

# 设置视角
ax.view_init(elev=10, azim=20)

# 添加图例
ax.legend()

# 设置图形标签
ax.set_xlabel('Recency')
ax.set_ylabel('Frequency')
ax.set_zlabel('Monetary')
ax.set_title('3D DBSCAN Clustering ')

# 保存图形，提升分辨率
plt.savefig(r"D:\PostGrduate\MINI\3D_DBSCAN_Clustering.png", dpi=600)
# 添加图例
ax.legend()

# 显示图形
plt.show()

# 准备存储每个季度的CLV分析结果
quarterly_cluster_analysis = {}

# 对每个季度进行DBSCAN聚类
for quarter in data['quarter'].unique():
    # 筛选当前季度的数据
    quarter_data = data[data['quarter'] == quarter].copy()
    quarter_scaled = scaler.transform(quarter_data[rfm_features])  # 使用相同的scaler对象进行变换

    # 使用DBSCAN聚类
    dbscan = DBSCAN(eps=1.5, min_samples=2)
    quarter_labels = dbscan.fit_predict(quarter_scaled)

    # 将标签添加到原始季度数据中
    quarter_data['Cluster'] = quarter_labels

    # 将更新后的季度数据合并回原始数据集
    data.loc[quarter_data.index, 'Cluster'] = quarter_labels

# 根据 'quarter' 和 'Cluster' 分组并计算聚类分析统计
cluster_analysis = data.groupby(['quarter', 'Cluster']).agg({
    'R': 'mean',
    'F': 'mean',
    'M': 'mean',
    'Account No': 'count'
}).rename(columns={'Account No': 'Count'}).reset_index()

# Min-Max标准化的正确方法
def min_max_normalize(data, group_columns, features):
    data_copy = data.copy()
    for feature in features:
        max_val = data_copy[feature].max()
        min_val = data_copy[feature].min()
        data_copy[feature + '_normalized'] = (data_copy[feature] - min_val) / (max_val - min_val)
    return data_copy

# Min-Max标准化
cluster_analysis_normalized = min_max_normalize(cluster_analysis, ['Cluster'], rfm_features)

# 应用标准化
normalized_features = ['R', 'F', 'M']
cluster_analysis = min_max_normalize(cluster_analysis, ['quarter', 'Cluster'], normalized_features)

# 计算权重
W_R = 0.6267
W_F = 0.2797
W_M = 0.0936

# 计算每个群集的CLV
cluster_analysis_normalized['CLV'] = (W_R * cluster_analysis_normalized['R_normalized'] +
                                      W_F * cluster_analysis_normalized['F_normalized'] +
                                      W_M * cluster_analysis_normalized['M_normalized'])

# 计算每个群集的客户百分比
total_customers = data['Account No'].nunique()
cluster_analysis_normalized['Percent of customer'] = (cluster_analysis_normalized['Count'] / total_customers) * 100

# 将当前季度的聚类分析结果存储起来
for quarter in data['quarter'].unique():
    quarterly_cluster_analysis[quarter] = cluster_analysis_normalized[cluster_analysis_normalized['quarter'] == quarter]

# 准备进行可视化的数据
clv_trends_data = {}

# 聚合每个季度的数据，准备进行趋势分析
for quarter, analysis in quarterly_cluster_analysis.items():
    clv_trends_data[quarter] = analysis.set_index('Cluster')['CLV']

# 将聚类趋势数据转换为DataFrame
clv_trends_df = pd.DataFrame(clv_trends_data).fillna(0)

# 可视化每个簇的CLV趋势
plt.figure(figsize=(10, 6))
for cluster in clv_trends_df.index:
    if cluster != -1:  # 排除噪声簇
        plt.plot(clv_trends_df.columns, clv_trends_df.loc[cluster], marker='o', label=f'Cluster {cluster}')
plt.title('CLV Trends per Cluster per Quarter')
plt.xlabel('Quarter')
plt.ylabel('CLV')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 假设 quarterly_cluster_analysis 已经正确填充了每个季度的数据
all_quarters_clv = pd.concat(quarterly_cluster_analysis.values(), ignore_index=True)

# 显示一些数据以确认其内容
print(all_quarters_clv.head())

# 将数据导出到CSV文件
all_quarters_clv.to_csv(r"D:\PostGrduate\MINI\quarterly_clv_data.csv", index=False)

data['Cluster'] = dbscan.fit_predict(data[rfm_features])
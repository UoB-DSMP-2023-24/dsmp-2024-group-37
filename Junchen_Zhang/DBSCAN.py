import pandas as pd
from sklearn.cluster import DBSCAN
import numpy as np
from sklearn.metrics import silhouette_score, pairwise_distances
from sklearn.preprocessing import StandardScaler

# 加载数据集
data = pd.read_csv(r"D:\PostGrduate\MINI\rfm_data.csv")

# 标准化整个数据集
scaler = StandardScaler()
rfm_features = ['R', 'F', 'M']
data_scaled = scaler.fit_transform(data[rfm_features])
data[rfm_features] = data_scaled

# 定义用于存储结果的字典
dbscan_clusters = {}
seasonal_dbscan_results = {}


def apply_dbscan(data, eps, min_samples):
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    return dbscan.fit_predict(data)

def dunn_index_corrected(distances, labels):
    # Assuming this function is now properly defined as discussed earlier
    unique_clusters = set(labels) - {-1}
    if len(unique_clusters) <= 1:
        return None

    intra_dists = np.array([np.max(distances[labels == k][:, labels == k]) for k in unique_clusters])
    inter_dists = np.inf

    for i in unique_clusters:
        for j in unique_clusters:
            if i != j:
                inter_dists = min(inter_dists, np.min(distances[labels == i][:, labels == j]))

    return inter_dists / np.max(intra_dists)

def find_best_params(data):
    # Define the range for DBSCAN parameters
    eps_range = np.linspace(0.1, 1.0, 10)
    min_samples_range = range(2, 10)
    best_score = -1
    best_params = None
    best_labels = None
    best_num_clusters = 0  # 初始化簇数量

    for eps in eps_range:
        for min_samples in min_samples_range:
            labels = apply_dbscan(data, eps, min_samples)
            num_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            if num_clusters > 1:  # 确保至少有两个簇
                score = silhouette_score(data, labels)
                if score > best_score:
                    best_score = score
                    best_params = (eps, min_samples)
                    best_labels = labels
                    best_num_clusters = num_clusters  # 更新最佳簇数量

    return best_params, best_labels, best_score, best_num_clusters

# 主处理流程
for quarter in data['quarter'].unique():
    quarter_data = data[data['quarter'] == quarter]
    quarter_scaled = quarter_data[rfm_features]

    best_params, best_labels, best_score, num_clusters = find_best_params(quarter_scaled)
    quarter_data.loc[:, 'Cluster'] = best_labels

    dbscan_clusters[quarter] = quarter_data

    distances = pairwise_distances(quarter_scaled)
    dunn_score = dunn_index_corrected(distances, best_labels)

    seasonal_dbscan_results[quarter] = {
        'params': best_params,
        'num_clusters': num_clusters,
        'dunn_index': dunn_score,
        'silhouette_score': best_score,
        'labels': best_labels
    }
# 输出每季度的DBSCAN结果和最佳参数
for quarter, results in seasonal_dbscan_results.items():
    print(f"Quarter {quarter}: Params: {results['params']}, Clusters: {results['num_clusters']}, Silhouette Score: {results['silhouette_score']}")
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, pairwise_distances
from sklearn.preprocessing import StandardScaler


# 加载数据集
data = pd.read_csv(r"D:\PostGrduate\MINI\rfm_data.csv")

# 标准化整个数据集
scaler = StandardScaler()
rfm_features = ['R', 'F', 'M']
data[rfm_features] = scaler.fit_transform(data[rfm_features])

def apply_dbscan(data, eps, min_samples):
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    return dbscan.fit_predict(data)

def find_best_params(data, target_clusters=2):
    # 定义DBSCAN参数范围
    eps_range = np.linspace(0.1, 2.0, 20)  # 增加eps的范围和精度
    min_samples_range = range(2, 10)
    best_score = -1
    best_params = None
    best_labels = None

    for eps in eps_range:
        for min_samples in min_samples_range:
            labels = apply_dbscan(data, eps, min_samples)
            num_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            if num_clusters == target_clusters:  # 目标是找到恰好三个簇的参数
                score = silhouette_score(data, labels)
                if score > best_score:
                    best_score = score
                    best_params = (eps, min_samples)
                    best_labels = labels

    return best_params, best_labels, best_score

# 在整个数据集上查找最佳参数
best_params, best_labels, best_score = find_best_params(data[rfm_features])

if best_params:
    print(f"Best Parameters: Epsilon: {best_params[0]}, Min_samples: {best_params[1]}")
    print(f"Silhouette Score: {best_score}")
    data['Cluster'] = best_labels
    data.to_csv(r"D:\PostGrduate\MINI\dbscan_clustered_data.csv", index=False)
else:
    print("No suitable parameter combination found for 3 clusters.")

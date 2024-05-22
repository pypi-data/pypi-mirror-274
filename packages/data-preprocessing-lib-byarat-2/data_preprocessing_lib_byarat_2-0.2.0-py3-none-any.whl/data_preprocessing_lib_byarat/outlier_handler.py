import pandas as pd
import numpy as np
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import DBSCAN

class OutlierHandler:
    @staticmethod
    def iqr_outlier_detection(df, column, threshold=1.5):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    
    @staticmethod
    def detect_outliers_iqr(df, column, threshold=1.5):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - (threshold * IQR)
        upper_bound = Q3 + (threshold * IQR)
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        return outliers

    @staticmethod
    def remove_outliers(df, column, threshold=1.5):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - (threshold * IQR)
        upper_bound = Q3 + (threshold * IQR)
        df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
        return df

    @staticmethod
    def z_score_outlier_detection(df, column, threshold=3):
        z_scores = np.abs(stats.zscore(df[column]))
        return df[z_scores < threshold]

    @staticmethod
    def detect_outliers_z_score(df, column, threshold=3):
        z_scores = np.abs(stats.zscore(df[column]))
        outliers = df[z_scores >= threshold]
        return outliers

    @staticmethod
    def remove_outliers_z_score(df, column, threshold=3):
        z_scores = np.abs(stats.zscore(df[column]))
        df = df[z_scores < threshold]
        return df

    @staticmethod
    def mad_outlier_detection(df, column, threshold=3):
        median = df[column].median()
        mad = np.median(np.abs(df[column] - median))
        modified_z_scores = 0.6745 * (df[column] - median) / mad
        return df[np.abs(modified_z_scores) < threshold]

    @staticmethod
    def detect_outliers_mad(df, column, threshold=3):
        median = df[column].median()
        mad = np.median(np.abs(df[column] - median))
        modified_z_scores = 0.6745 * (df[column] - median) / mad
        outliers = df[np.abs(modified_z_scores) >= threshold]
        return outliers

    @staticmethod
    def remove_outliers_mad(df, column, threshold=3):
        median = df[column].median()
        mad = np.median(np.abs(df[column] - median))
        modified_z_scores = 0.6745 * (df[column] - median) / mad
        df = df[np.abs(modified_z_scores) < threshold]
        return df

    @staticmethod
    def mahalanobis_outlier_detection(df, columns, threshold=3):
        x = df[columns].values
        x_mean = np.mean(x, axis=0)
        x_cov = np.cov(x, rowvar=False)
        x_inv_cov = np.linalg.inv(x_cov)
        x_diff = x - x_mean
        mahalanobis_dist = np.sqrt(np.sum(np.dot(x_diff, x_inv_cov) * x_diff, axis=1))
        return df[mahalanobis_dist < threshold]

    @staticmethod
    def detect_outliers_mahalanobis(df, columns, threshold=3):
        x = df[columns].values
        x_mean = np.mean(x, axis=0)
        x_cov = np.cov(x, rowvar=False)
        x_inv_cov = np.linalg.inv(x_cov)
        x_diff = x - x_mean
        mahalanobis_dist = np.sqrt(np.sum(np.dot(x_diff, x_inv_cov) * x_diff, axis=1))
        outliers = df[mahalanobis_dist >= threshold]
        return outliers

    @staticmethod
    def remove_outliers_mahalanobis(df, columns, threshold=3):
        x = df[columns].values
        x_mean = np.mean(x, axis=0)
        x_cov = np.cov(x, rowvar=False)
        x_inv_cov = np.linalg.inv(x_cov)
        x_diff = x - x_mean
        mahalanobis_dist = np.sqrt(np.sum(np.dot(x_diff, x_inv_cov) * x_diff, axis=1))
        df = df[mahalanobis_dist < threshold]
        return df

    @staticmethod
    def tukeys_fences_outlier_detection(df, column, k=1.5):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - k * IQR
        upper_bound = Q3 + k * IQR
        return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

    @staticmethod
    def detect_outliers_tukeys_fences(df, column, k=1.5):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - k * IQR
        upper_bound = Q3 + k * IQR
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        return outliers

    @staticmethod
    def remove_outliers_tukeys_fences(df, column, k=1.5):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - k * IQR
        upper_bound = Q3 + k * IQR
        df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
        return df

    @staticmethod
    def isolation_forest_outlier_detection(df, column, contamination=0.1):
        isolation_forest = IsolationForest(contamination=contamination)
        isolation_forest.fit(df[[column]])
        df['anomaly'] = isolation_forest.predict(df[[column]])
        return df[df['anomaly'] == 1].drop(columns=['anomaly'])

    @staticmethod
    def detect_outliers_isolation_forest(df, column, contamination=0.1):
        isolation_forest = IsolationForest(contamination=contamination)
        isolation_forest.fit(df[[column]])
        df['anomaly'] = isolation_forest.predict(df[[column]])
        outliers = df[df['anomaly'] == -1]
        return outliers.drop(columns=['anomaly'])

    @staticmethod
    def remove_outliers_isolation_forest(df, column, contamination=0.1):
        isolation_forest = IsolationForest(contamination=contamination)
        isolation_forest.fit(df[[column]])
        df['anomaly'] = isolation_forest.predict(df[[column]])
        df = df[df['anomaly'] == 1].drop(columns=['anomaly'])
        return df

    @staticmethod
    def local_outlier_factor_detection(df, column, n_neighbors=20, contamination=0.1):
        lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination)
        lof.fit(df[[column]])
        df['anomaly'] = lof.fit_predict(df[[column]])
        return df[df['anomaly'] == 1].drop(columns=['anomaly'])

    @staticmethod
    def detect_outliers_local_outlier_factor(df, column, n_neighbors=20, contamination=0.1):
        lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination)
        lof.fit(df[[column]])
        df['anomaly'] = lof.fit_predict(df[[column]])
        outliers = df[df['anomaly'] == -1]
        return outliers.drop(columns=['anomaly'])

    @staticmethod
    def remove_outliers_local_outlier_factor(df, column, n_neighbors=20, contamination=0.1):
        lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination)
        lof.fit(df[[column]])
        df['anomaly'] = lof.fit_predict(df[[column]])
        df = df[df['anomaly'] == 1].drop(columns=['anomaly'])
        return df

    @staticmethod
    def dbscan_outlier_detection(df, column, eps=0.5, min_samples=5):
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        df['anomaly'] = dbscan.fit_predict(df[[column]])
        return df[df['anomaly'] != -1].drop(columns=['anomaly'])

    @staticmethod
    def detect_outliers_dbscan(df, column, eps=0.5, min_samples=5):
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        df['anomaly'] = dbscan.fit_predict(df[[column]])
        outliers = df[df['anomaly'] == -1]
        return outliers.drop(columns=['anomaly'])

    @staticmethod
    def remove_outliers_dbscan(df, column, eps=0.5, min_samples=5):
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        df['anomaly'] = dbscan.fit_predict(df[[column]])
        df = df[df['anomaly'] != -1].drop(columns=['anomaly'])
        return df

# Test kodu
if __name__ == "__main__":
    data = {
        'value': [1, 2, 3, 4, 5, 100, 101, 102, 103, 104],
        'value2': [10, 20, 30, 40, 50, 1000, 2000, 3000, 4000, 5000]
    }
    df = pd.DataFrame(data)

    handler = OutlierHandler()

    # IQR outlier detection test
    df_iqr = handler.iqr_outlier_detection(df.copy(), 'value')
    print("IQR Outlier Detection:")
    print(df_iqr)

    # Z-score outlier detection test
    df_z_score = handler.z_score_outlier_detection(df.copy(), 'value')
    print("Z-score Outlier Detection:")
    print(df_z_score)

    # MAD outlier detection test
    df_mad = handler.mad_outlier_detection(df.copy(), 'value')
    print("MAD Outlier Detection:")
    print(df_mad)

    # Mahalanobis outlier detection test
    df_mahalanobis = handler.mahalanobis_outlier_detection(df.copy(), ['value', 'value2'])
    print("Mahalanobis Outlier Detection:")
    print(df_mahalanobis)

    # Tukey's fences outlier detection test
    df_tukey = handler.tukeys_fences_outlier_detection(df.copy(), 'value')
    print("Tukey's Fences Outlier Detection:")
    print(df_tukey)

    # Isolation Forest outlier detection test
    df_isolation_forest = handler.isolation_forest_outlier_detection(df.copy(), 'value')
    print("Isolation Forest Outlier Detection:")
    print(df_isolation_forest)

    # Local Outlier Factor detection test
    df_lof = handler.local_outlier_factor_detection(df.copy(), 'value')
    print("Local Outlier Factor Detection:")
    print(df_lof)

    # DBSCAN outlier detection test
    df_dbscan = handler.dbscan_outlier_detection(df.copy(), 'value')
    print("DBSCAN Outlier Detection:")
    print(df_dbscan)

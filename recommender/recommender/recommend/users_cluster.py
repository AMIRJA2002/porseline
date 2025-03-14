from sklearn.cluster import KMeans
import pandas as pd


def prepare_user_features(users_df: pd.DataFrame, browsing_df: pd.DataFrame, purchase_df: pd.DataFrame) -> pd.DataFrame:
    user_features = users_df[["user_id", "location", "device"]]

    user_features = pd.get_dummies(user_features, columns=["location", "device"])

    user_view_counts = browsing_df.groupby('user_id').size().reset_index(name='view_count')
    user_features = user_features.merge(user_view_counts, on='user_id', how='left')

    user_purchase_counts = purchase_df.groupby('user_id').size().reset_index(name='purchase_count')
    user_features = user_features.merge(user_purchase_counts, on='user_id', how='left')

    user_features = user_features.fillna(0)

    return user_features


def cluster_users(user_features: pd.DataFrame) -> pd.DataFrame:
    kmeans = KMeans(n_clusters=10, random_state=42, n_init=10)

    user_features = user_features.copy()
    user_features["cluster"] = kmeans.fit_predict(user_features.drop(columns=["user_id"]))

    print(user_features[["user_id", "cluster"]].head(10))

    return user_features[["user_id", "cluster"]]

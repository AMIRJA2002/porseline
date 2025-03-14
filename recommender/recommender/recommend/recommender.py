from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import pandas as pd

weights = {
    "viewed_or_carted": 0.3,
    "similar_users": 0.3,
    "popular_trending": 0.2,
    "personalization": 0.1,
    "contextual": 0.1
}


def get_contextual_signals(timestamp):
    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    hour = dt.hour
    day_of_week = dt.strftime("%A")
    month = dt.month

    if 6 <= hour < 12:
        time_of_day = "morning"
    elif 12 <= hour < 18:
        time_of_day = "afternoon"
    else:
        time_of_day = "evening"

    if month in [12, 1, 2]:
        season = "winter"
    elif month in [3, 4, 5]:
        season = "spring"
    elif month in [6, 7, 8]:
        season = "summer"
    else:
        season = "autumn"

    return {"time_of_day": time_of_day, "day_of_week": day_of_week, "season": season}


def calculate_final_score(
        user_id: int,
        product_id: int,
        purchase_df: pd.DataFrame,
        browsing_df: pd.DataFrame,
        products_df: pd.DataFrame,
        timestamp: str,
):
    reasons = []
    user_product_matrix = pd.pivot_table(purchase_df, values='quantity', index='user_id', columns='product_id',
                                         fill_value=0)
    user_similarity = cosine_similarity(user_product_matrix)
    user_similarity_df = pd.DataFrame(
        user_similarity,
        index=user_product_matrix.index,
        columns=user_product_matrix.index
    )

    viewed_or_carted_score = 1 if product_id in browsing_df[browsing_df["user_id"] == user_id][
        "product_id"].values else 0
    if viewed_or_carted_score:
        reasons.append("you seen or add this product to your basket.")

    if user_id in user_similarity_df.columns:
        similar_users = user_similarity_df[user_id].sort_values(ascending=False).iloc[1:3].index.tolist()
    else:
        similar_users = []

    similar_users_products = purchase_df[purchase_df["user_id"].isin(similar_users)]["product_id"].unique()
    similar_users_score = 1 if product_id in similar_users_products else 0
    if similar_users_score:
        reasons.append("similar users bought this product.")

    popular_products = purchase_df["product_id"].value_counts().index[:3]
    popular_trending_score = 1 if product_id in popular_products else 0
    if popular_trending_score:
        reasons.append("product is popular or trend.")

    user_categories = purchase_df[purchase_df["user_id"] == user_id].merge(products_df, on="product_id")[
        "category"].unique()
    product_category = products_df[products_df["product_id"] == product_id]["category"].values[0]
    personalization_score = 1 if product_category in user_categories else 0
    if personalization_score:
        reasons.append(f"you bought products from '{product_category}' category.")

    contextual_signals = get_contextual_signals(timestamp)
    product_tags = products_df[products_df["product_id"] == product_id]["tags"].values[0]
    contextual_score = 0

    if contextual_signals["season"] in product_tags:
        contextual_score = 1
        reasons.append(f"this product is suitable {contextual_signals['season']} for the season.")
    if contextual_signals["time_of_day"] in product_tags:
        contextual_score = 1
        reasons.append(f"this product is suitable {contextual_signals['time_of_day']} at this time.")

    final_score = (
            weights["viewed_or_carted"] * viewed_or_carted_score +
            weights["similar_users"] * similar_users_score +
            weights["popular_trending"] * popular_trending_score +
            weights["personalization"] * personalization_score +
            weights["contextual"] * contextual_score
    )
    return final_score, reasons

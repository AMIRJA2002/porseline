from recommender.recommend.models import Product
from recommender.recommend.recommender import calculate_final_score
import pandas as pd


def recommend_products_services(
        user_id: int,
        browsing_df: pd.DataFrame,
        products_df: pd.DataFrame,
        purchase_df: pd.DataFrame,
        timestamp: str,
        top_n: int = 3
):
    recommendations = {
        "user_id": user_id,
        "timestamp": timestamp,
        "recommended_products": []
    }

    # check for user interaction
    if products_df.empty or browsing_df.empty or user_id not in purchase_df["user_id"].values and user_id not in \
            browsing_df["user_id"].values:
        print(f"user {user_id} has no new interaction:")

        random_products = Product.objects.all().order_by('-rating')[:top_n]

        for _, row in random_products.iterrows():
            recommendations["recommended_products"].append({
                "product_name": row["name"],
                "score": None,
                "reasons": ["populat products, selection due to lack of user interaction"]
            })

        return recommendations

    product_scores = []
    for product in products_df["product_id"]:
        score, reasons = calculate_final_score(user_id=user_id, product_id=product,
                                               browsing_df=browsing_df, products_df=products_df,
                                               purchase_df=purchase_df, timestamp=timestamp)
        product_scores.append({"product_id": product, "score": score, "reasons": reasons})

    product_scores_df = pd.DataFrame(product_scores)
    product_scores_df = product_scores_df.sort_values(by="score", ascending=False)

    for i, row in product_scores_df.head(top_n).iterrows():
        product_name = products_df[products_df["product_id"] == row["product_id"]]["name"].values[0]
        recommendations["recommended_products"].append({
            "product_name": product_name,
            "score": round(row["score"], 2),
            "reasons": row["reasons"] if row["reasons"] else "This product was not suggested with known parameter."
        })

    return recommendations

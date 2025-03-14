from .models import User, BrowsingHistory, PurchaseHistory, Product
from django.utils import timezone
from datetime import timedelta


def get_users_for_cluster() -> list[dict[str, any]]:
    users = User.objects.all().values("id", "name", "location", "device")
    users_list = [
        {
            "user_id": user["id"],
            "name": user["name"],
            "location": user["location"],
            "device": user["device"]
        }
        for user in users
    ]
    return users_list


def get_browsing_history_for_cluster() -> list[dict[str, any]]:
    browsing_history = BrowsingHistory.objects.all().values("user_id", "product_id", "timestamp")
    browsing_history_list = [
        {
            "user_id": entry["user_id"],
            "product_id": entry["product_id"],
            "timestamp": entry["timestamp"]
        }
        for entry in browsing_history
    ]
    return browsing_history_list


def get_purchase_history_for_cluster() -> list[dict[str, any]]:
    purchase_history = PurchaseHistory.objects.all().values("user_id", "product_id", "quantity", "timestamp")
    purchase_history_list = [
        {
            "user_id": entry["user_id"],
            "product_id": entry["product_id"],
            "quantity": entry["quantity"],
            "timestamp": entry["timestamp"]
        }
        for entry in purchase_history
    ]
    return purchase_history_list


def get_products_for_cluster() -> list[dict[str, any]]:
    products = Product.objects.all().values("id", "name", "category", "tags", "rating")
    products_list = [
        {
            "product_id": product["id"],
            "name": product["name"],
            "category": product["category"],
            "tags": product["tags"],
            "rating": product["rating"]
        }
        for product in products
    ]
    return products_list


def get_browsing_history_for_recommend(user_cluster: int) -> list[dict[str, any]]:
    thirty_days_ago = timezone.now() - timedelta(days=30)
    users_in_cluster = User.objects.filter(cluster=user_cluster)
    browsing_history = BrowsingHistory.objects.filter(
        user__in=users_in_cluster,
        timestamp__gte=thirty_days_ago  # فقط تاریخ‌های ۳۰ روز گذشته
    ).values("user_id", "product_id", "timestamp")
    browsing_history_list = [
        {
            "user_id": entry["user_id"],
            "product_id": entry["product_id"],
            "timestamp": entry["timestamp"]
        }
        for entry in browsing_history
    ]
    return browsing_history_list


def get_purchase_history_for_recommend(user_cluster: int) -> list[dict[str, any]]:
    thirty_days_ago = timezone.now() - timedelta(days=30)
    users_in_cluster = User.objects.filter(cluster=user_cluster)
    purchase_history = PurchaseHistory.objects.filter(
        user__in=users_in_cluster,
        timestamp__gte=thirty_days_ago  # فقط تاریخ‌های ۳۰ روز گذشته
    ).values("user_id", "product_id", "quantity", "timestamp")
    purchase_history_list = [
        {
            "user_id": entry["user_id"],
            "product_id": entry["product_id"],
            "quantity": entry["quantity"],
            "timestamp": entry["timestamp"]
        }
        for entry in purchase_history
    ]
    return purchase_history_list

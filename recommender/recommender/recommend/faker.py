from recommender.recommend.models import BrowsingHistory, PurchaseHistory, ContextualSignal, User, Product
from random import randint, choice
from faker import Faker
import json

fake = Faker()

num_records = 50


def create_users():
    for _ in range(num_records):
        User.objects.create(
            name=fake.name(),
            location=fake.city(),
            device=choice(["mobile", "desktop"])
        )


def create_products():
    categories = ["Electronics", "Accessories", "Fitness", "Personal Care", "Office Supplies"]
    for _ in range(num_records):
        Product.objects.create(
            name=fake.word() + " " + fake.word(),
            category=choice(categories),
            tags=json.dumps([fake.word() for _ in range(3)]),
            rating=round(randint(30, 50) / 10, 1)
        )


def create_browsing_history():
    for _ in range(num_records):
        user_id = randint(1, num_records)
        product_id = randint(1, num_records)
        BrowsingHistory.objects.create(
            user_id=user_id,
            product_id=product_id,
            timestamp=fake.date_time_this_year()
        )


def create_purchase_history():
    for _ in range(num_records):
        user_id = randint(1, num_records)
        product_id = randint(1, num_records)
        PurchaseHistory.objects.create(
            user_id=user_id,
            product_id=product_id,
            quantity=randint(1, 5),
            timestamp=fake.date_time_this_year()
        )


def create_contextual_signals():
    categories = ["Electronics", "Accessories", "Fitness", "Personal Care", "Office Supplies"]
    for _ in range(num_records):
        ContextualSignal.objects.create(
            category=choice(categories),
            peak_days=json.dumps([randint(1, 7) for _ in range(3)]),
            season=choice(["Summer", "Winter", "Spring", "Autumn"])
        )

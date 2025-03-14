from recommender.recommend.models import (
    User,
    Product,
    BrowsingHistory,
    PurchaseHistory,
    ContextualSignal,
)

from django.contrib import admin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "location", "device")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "rating")


@admin.register(BrowsingHistory)
class BrowsingHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "timestamp")
    list_filter = ("timestamp",)


@admin.register(PurchaseHistory)
class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "timestamp")
    list_filter = ("timestamp",)


@admin.register(ContextualSignal)
class ContextualSignalAdmin(admin.ModelAdmin):
    list_display = ("category", "season")

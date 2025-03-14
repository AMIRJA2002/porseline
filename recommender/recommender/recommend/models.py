from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    device = models.CharField(max_length=50)
    cluster = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    tags = models.JSONField()
    rating = models.FloatField()

    def __str__(self):
        return self.name


class BrowsingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.user.name}-{self.product.name}"


class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.user.name}-{self.quantity}-{self.product.name}"


class ContextualSignal(models.Model):
    category = models.CharField(max_length=100)
    peak_days = models.JSONField()
    season = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category}-{self.season}"

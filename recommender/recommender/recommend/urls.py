from django.urls import path
from .views import FakerData, TestQuery, ProductRecommender

urlpatterns = [
    path('faker/', FakerData.as_view()),
    path('test/', TestQuery.as_view()),
    path('recommend/', ProductRecommender.as_view()),
]

from django.urls import path, include

urlpatterns = [
    path('', include(('recommender.recommend.urls', 'recommend')))
]

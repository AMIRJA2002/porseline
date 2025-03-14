from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from functools import wraps
import redis
import json

redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)


def cache_user_recommends(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        number_of_product = request.data.get('number_of_product')

        cache_key = f"user_{user_id}_products_{number_of_product}"
        cached_response = redis_client.get(cache_key)

        if cached_response:
            cached_data = json.loads(cached_response)
            return Response(cached_data, status=status.HTTP_200_OK)

        response = func(self, request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            redis_client.setex(cache_key, timedelta(hours=3), json.dumps(response.data))

        return response

    return wrapper

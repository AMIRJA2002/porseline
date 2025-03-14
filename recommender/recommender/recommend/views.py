from recommender.recommend.cache_decorator import cache_user_recommends
from recommender.recommend.services import recommend_products_services
from recommender.recommend.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status
from datetime import datetime

from recommender.recommend.data_frames import (
    create_browsing_history_data_frame,
    create_product_data_frame,
    create_purchase_data_frame,
)
from recommender.recommend.faker import (
    create_contextual_signals,
    create_browsing_history,
    create_purchase_history,
    create_products,
    create_users,
)
from recommender.recommend.selectors import (
    get_products_for_cluster,
    get_browsing_history_for_recommend,
    get_purchase_history_for_recommend
)


class FakerData(APIView):
    def get(self, request):
        create_users()
        create_products()
        create_browsing_history()
        create_purchase_history()
        create_contextual_signals()

        return Response({'mgs': 'ok'})


class ProductRecommender(APIView):
    class RecommenderInputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        number_of_product = serializers.IntegerField(max_value=50)

    @cache_user_recommends
    def get(self, request):
        try:
            data = self.RecommenderInputSerializer(data=request.data)
            data.is_valid(raise_exception=True)
            user_id = int(data.validated_data['user_id'])
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user = User.objects.get(id=user_id)
            data = recommend_products_services(
                user_id=user_id,
                browsing_df=create_browsing_history_data_frame(get_browsing_history_for_recommend(user.cluster)),
                products_df=create_product_data_frame(get_products_for_cluster()),
                purchase_df=create_purchase_data_frame(get_purchase_history_for_recommend(user.cluster)),
                timestamp=current_time,
                top_n=data.validated_data['number_of_product'],
            )

            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'something went wrong!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestQuery(APIView):
    def get(self, request):
        pass

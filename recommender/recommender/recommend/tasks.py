from django.utils.timezone import now
from celery import shared_task
from .models import User
from .selectors import(
    get_browsing_history_for_cluster,
    get_purchase_history_for_cluster,
    get_users_for_cluster,
)

from .data_frames import (
    create_browsing_history_data_frame,
    create_purchase_data_frame,
    create_user_data_frame,
)

from .users_cluster import(
    prepare_user_features,
    cluster_users
)

@shared_task
def cluster_users_task():
    user_data_frame = create_user_data_frame(get_users_for_cluster())
    browsing_data_frame = create_browsing_history_data_frame(get_browsing_history_for_cluster())
    purchase_data_frame = create_purchase_data_frame(get_purchase_history_for_cluster())

    user_features = prepare_user_features(user_data_frame, browsing_data_frame, purchase_data_frame)
    users_list = cluster_users(user_features)

    for _, row in users_list.iterrows():
        User.objects.filter(id=row["user_id"]).update(cluster=row["cluster"])

    return f"User clustering completed successfully at {now()}."

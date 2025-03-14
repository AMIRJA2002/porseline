from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.core.management.base import BaseCommand
from celery.schedules import crontab
from django.core.exceptions import ValidationError
import json


class Command(BaseCommand):
    help = "create schedule task for clustering users"

    def handle(self, *args, **kwargs):
        try:
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=24, period=IntervalSchedule.HOURS
            )

            task, created = PeriodicTask.objects.get_or_create(
                name="Cluster Users Daily",
                interval=schedule,
                task="recommender.recommend.tasks.cluster_users_task",
                defaults={"kwargs": json.dumps({})},
            )

            self.stdout.write(self.style.SUCCESS("task created."))
        except ValidationError:
            self.stdout.write(self.style.WARNING("task already exists."))

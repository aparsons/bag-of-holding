from django.contrib.contenttypes.models import ContentType
from django.db import models


class EventManager(models.Manager):
    pass


class FollowManager(models.Manager):
    def create_follow(self, user, actor):
        return self.create(user=user, actor_type=ContentType.objects.get_for_model(actor), actor_id=actor.id)


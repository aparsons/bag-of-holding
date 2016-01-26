from django.contrib.contenttypes.models import ContentType
from django.db import models


class EventManager(models.Manager):
    def create_event(self, actor, verb, action=None, preposition=None, target=None, public=True):
        actor_type = ContentType.objects.get_for_model(actor)
        if target:
            target_type = ContentType.objects.get_for_model(target)
            if action:
                action_type = ContentType.objects.get_for_model(action)
                return self.create(actor_type=actor_type, actor_id=actor.id, verb=verb, action_type=action_type, action_id=action.id, preposition=preposition, target_type=target_type, target_id=target.id, public=public)
            return self.create(actor_type=actor_type, actor_id=actor.id, verb=verb, target_type=target_type, target_id=target.id, public=public)
        if action:
            action_type = ContentType.objects.get_for_model(action)
            return self.create(actor_type=actor_type, actor_id=actor.id, verb=verb, action_type=action_type, action_id=action.id, public=public)
        return self.create(actor_type=actor_type, actor_id=actor.id, verb=verb, public=public)


class FollowManager(models.Manager):
    def create_follow(self, user, actor):
        return self.create(user=user, actor_type=ContentType.objects.get_for_model(actor), actor_id=actor.id)

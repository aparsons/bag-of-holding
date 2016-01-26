from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q


class EventQuerySet(models.QuerySet):
    def public(self, **kwargs):
        """Returns public events only."""
        return self.filter(public=True, **kwargs)

    def actor(self, obj, **kwargs):
        """Returns public events by actor."""
        return self.public().filter(actor_type=ContentType.objects.get_for_model(obj), actor_id=obj.id, **kwargs)

    def action(self, obj, **kwargs):
        """Returns public events by action."""
        return self.public().filter(action_type=ContentType.objects.get_for_model(obj), action_id=obj.id, **kwargs)

    def target(self, obj, **kwargs):
        """Returns public events by target."""
        return self.public().filter(target_type=ContentType.objects.get_for_model(obj), target_id=obj.id, **kwargs)

    def any(self, obj, **kwargs):
        """Returns public events where the object is the actor, action, or target."""
        content_type = ContentType.objects.get_for_model(obj)
        return self.public().filter(
            Q(actor_type=content_type, actor_id=obj.id) | Q(action_type=content_type, action_id=obj.id) | Q(target_type=content_type, target_id=obj.id)
        )

class FollowQuerySet(models.QuerySet):
    pass

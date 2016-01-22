from django.db import models


class ActionQuerySet(models.QuerySet):
    def public(self):
        """Returns public actions only."""
        return self.filter(public=True)


class FollowQuerySet(models.QuerySet):
    pass

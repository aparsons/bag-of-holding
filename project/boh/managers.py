import datetime

from django.db import models
from django.db.models import Avg, Case, Count, IntegerField, Prefetch, Q, Sum, When


class ApplicationManager(models.Manager):
    pass


class ApplicationQuerySet(models.QuerySet):
    def requestable(self):
        """Returns Applications permitting external activity requests."""
        return self.filter(requestable=True)

    def threadfix_associated(self):
        """Returns Applications that have all the ThreadFix configurations set."""
        return self.exclude(threadfix__isnull=True).exclude(threadfix_team_id__isnull=True).exclude(threadfix_application_id__isnull=True)


class ActivityTypeManager(models.Manager):
    pass


class ActivityTypeMetrics(models.Manager):
    def stats(self, year=None):
        """Returns counts of each activity and their average durations."""
        from .models import Activity
        results = self.get_queryset()

        activity_queryset = Activity.objects.all()
        if year:
            activity_queryset = activity_queryset.filter(open_date__year=year)

        results = results.prefetch_related(Prefetch('activity_set', queryset=activity_queryset))
        results = results.annotate(
            pending_count=Sum(
                Case(When(activity__status=Activity.PENDING_STATUS, then=1), output_field=IntegerField(), default=0)
            ),
            open_count=Sum(
                Case(When(activity__status=Activity.OPEN_STATUS, then=1), output_field=IntegerField(), default=0)
            ),
            closed_count=Sum(
                Case(When(activity__status=Activity.CLOSED_STATUS, then=1), output_field=IntegerField(), default=0)
            )
        )
        results = results.annotate(total_count=Count('activity__status'))
        results = results.annotate(average_duration=Avg('activity__duration'))

        # Convert duration averages into timedelta
        for result in results:
            if result.average_duration:
                result.average_duration = datetime.timedelta(microseconds=result.average_duration)

        return results


class ActivityTypeQuerySet(models.QuerySet):
    pass


class EngagementManager(models.Manager):
    def distinct_years(self):
        """Returns a list of distinct years by open_date."""
        results = self.get_queryset()
        results = results.datetimes('open_date', 'year')

        years_list = []

        for result in results:
            years_list.append(result.year)

        return years_list


class EngagementMetrics(models.Manager):
    def stats(self, year=None):
        """Returns counts for each Engagement status and the average duration."""
        from .models import Engagement
        results = self.get_queryset()

        if year:
            results = results.filter(open_date__year=year)

        results = results.aggregate(
            pending_count=Sum(
                Case(When(status=Engagement.PENDING_STATUS, then=1), output_field=IntegerField(), default=0)
            ),
            open_count=Sum(
                Case(When(status=Engagement.OPEN_STATUS, then=1), output_field=IntegerField(), default=0)
            ),
            closed_count=Sum(
                Case(When(status=Engagement.CLOSED_STATUS, then=1), output_field=IntegerField(), default=0)
            ),
            total_count=Count('id'),
            average_duration=Avg('duration')
        )

        if results['average_duration']:
            results['average_duration'] = datetime.timedelta(microseconds=results['average_duration'])

        return results


class EngagementQuerySet(models.QuerySet):
    def closed(self):
        """Returns Engagements with a closed status."""
        from .models import Engagement
        return self.filter(status=Engagement.CLOSED_STATUS)


class ActivityManager(models.Manager):
    def distinct_years(self):
        """Returns a list of distinct years by open_date."""
        results = self.get_queryset()
        results = results.datetimes('open_date', 'year')

        years_list = []

        for result in results:
            years_list.append(result.year)

        return years_list


class ActivityQuerySet(models.QuerySet):
    def closed(self):
        """Returns Activities with a closed status."""
        from .models import Activity
        return self.filter(status=Activity.CLOSED_STATUS)

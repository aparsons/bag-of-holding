# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import uuid


def update_durations(apps, schema_editor):
    """This will update the duration fields for pre-existing engagements and activities."""
    # Update Engagements
    Engagement = apps.get_model('boh', 'Engagement')
    engagements = Engagement.objects.exclude(open_date__isnull=True).exclude(close_date__isnull=True)
    for engagement in engagements:
        engagement.save()

    # Update Activities
    Activity = apps.get_model('boh', 'Activity')
    activities = Activity.objects.exclude(open_date__isnull=True).exclude(close_date__isnull=True)
    for activity in activities:
        activity.save()

class Migration(migrations.Migration):

    dependencies = [
        ('boh', '0004_v1_0_2'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ThreadFixMetrics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('critical_count', models.PositiveIntegerField(default=0)),
                ('high_count', models.PositiveIntegerField(default=0)),
                ('medium_count', models.PositiveIntegerField(default=0)),
                ('low_count', models.PositiveIntegerField(default=0)),
                ('informational_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'ThreadFix metrics',
                'verbose_name_plural': 'ThreadFix metrics',
                'get_latest_by': 'created_date',
            },
        ),
        migrations.AlterModelOptions(
            name='engagement',
            options={'get_latest_by': 'close_date', 'ordering': ['start_date']},
        ),
        migrations.AddField(
            model_name='activity',
            name='duration',
            field=models.DurationField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='activitytype',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 26, 13, 4, 15, 781334, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activitytype',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 26, 13, 4, 23, 524634, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activitytype',
            name='requestable',
            field=models.NullBooleanField(default=False, help_text='Specify if this activity type can be externally requested.'),
        ),
        migrations.AddField(
            model_name='application',
            name='requestable',
            field=models.NullBooleanField(default=True, help_text='Specify if activities can be externally requested for this application.'),
        ),
        migrations.AddField(
            model_name='engagement',
            name='duration',
            field=models.DurationField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='data_elements',
            field=models.ManyToManyField(to='boh.DataElement', blank=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='regulations',
            field=models.ManyToManyField(to='boh.Regulation', blank=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='service_level_agreements',
            field=models.ManyToManyField(to='boh.ServiceLevelAgreement', blank=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='technologies',
            field=models.ManyToManyField(to='boh.Technology', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(max_length=128, unique=True),
        ),
        migrations.AddField(
            model_name='threadfixmetrics',
            name='application',
            field=models.ForeignKey(to='boh.Application'),
        ),
        migrations.AddField(
            model_name='externalrequest',
            name='activities',
            field=models.ManyToManyField(to='boh.ActivityType'),
        ),
        migrations.AddField(
            model_name='externalrequest',
            name='application',
            field=models.ForeignKey(to='boh.Application', blank=True),
        ),
        migrations.AddField(
            model_name='externalrequest',
            name='requestor',
            field=models.ForeignKey(to='boh.Person'),
        ),
        migrations.RunPython(update_durations),
    ]

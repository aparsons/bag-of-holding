# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boh', '0002_load_data'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activitytype',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='application',
            name='threadfix_organization_id',
        ),
        migrations.AddField(
            model_name='application',
            name='threadfix_team_id',
            field=models.PositiveIntegerField(blank=True, help_text='The unique team identifier used within ThreadFix.', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relation',
            name='emergency',
            field=models.BooleanField(help_text='Specify if this person is an emergency contact.', default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tag',
            name='description',
            field=models.CharField(blank=True, max_length=64, help_text="A short description of this tag's purpose to be shown in tooltips."),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='threadfix',
            name='verify_ssl',
            field=models.BooleanField(help_text="Specify if API requests will verify the host's SSL certificate. If disabled, API requests could be intercepted by third-parties.", default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activitytype',
            name='name',
            field=models.CharField(max_length=128, help_text='A unique name for this activity type.', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='application',
            name='organization',
            field=models.ForeignKey(to='boh.Organization', help_text='The organization containing this application.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='application',
            name='threadfix',
            field=models.ForeignKey(to='boh.ThreadFix', null=True, blank=True, help_text='The ThreadFix service to connect to this application.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='application',
            name='threadfix_application_id',
            field=models.PositiveIntegerField(blank=True, help_text='The unique application identifier used within ThreadFix.', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='engagement',
            name='requestor',
            field=models.ForeignKey(to='boh.Person', null=True, blank=True, help_text='Specify who requested this engagement.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(max_length=75, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='relation',
            name='notes',
            field=models.TextField(blank=True, help_text="Any notes about this person's connection to the application."),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='relation',
            name='owner',
            field=models.BooleanField(help_text='Specify if this person is an application owner.', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='relation',
            name='person',
            field=models.ForeignKey(to='boh.Person', help_text='The person associated with the application.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='threadfix',
            name='name',
            field=models.CharField(max_length=32, help_text='A unique name describing the ThreadFix service.', unique=True),
            preserve_default=True,
        ),
    ]

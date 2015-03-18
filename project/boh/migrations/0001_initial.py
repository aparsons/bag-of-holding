# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('status', models.CharField(max_length=7, default='pending', choices=[('pending', 'Pending'), ('open', 'Open'), ('closed', 'Closed')])),
                ('description', models.TextField(blank=True)),
                ('open_date', models.DateTimeField(blank=True, help_text='The date and time when the status is changed to open.', null=True)),
                ('close_date', models.DateTimeField(blank=True, help_text='The date and time when the status is changed to closed.', null=True)),
            ],
            options={
                'verbose_name_plural': 'Activities',
                'ordering': ['engagement__start_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActivityComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('message', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('activity', models.ForeignKey(to='boh.Activity')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActivityType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=128, help_text='A unique name for this activity.', unique=True)),
                ('documentation', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=128, help_text='A unique name for the application.', unique=True)),
                ('description', models.TextField(blank=True, help_text="Information about the application's purpose, history, and design.")),
                ('platform', models.CharField(max_length=11, null=True, blank=True, choices=[(None, 'Not Specified'), ('web', 'Web'), ('desktop', 'Desktop'), ('mobile', 'Mobile'), ('web service', 'Web Service')])),
                ('lifecycle', models.CharField(max_length=8, null=True, blank=True, choices=[(None, 'Not Specified'), ('idea', 'Idea'), ('explore', 'Explore'), ('validate', 'Validate'), ('grow', 'Grow'), ('sustain', 'Sustain'), ('retire', 'Retire')])),
                ('origin', models.CharField(max_length=19, null=True, blank=True, choices=[(None, 'Not Specified'), ('third party library', 'Third Party Library'), ('purchased', 'Purchased'), ('contractor', 'Contractor'), ('internal', 'Internally Developed'), ('open source', 'Open Source'), ('outsourced', 'Outsourced')])),
                ('business_criticality', models.CharField(max_length=9, null=True, blank=True, choices=[(None, 'Not Specified'), ('very high', 'Very High'), ('high', 'High'), ('medium', 'Medium'), ('low', 'Low'), ('very low', 'Very Low'), ('none', 'None')])),
                ('users_records', models.PositiveIntegerField(blank=True, help_text='Estimate the number of user records within the application.', null=True)),
                ('revenue', models.DecimalField(blank=True, max_digits=15, decimal_places=2, help_text="Estimate the application's revenue in USD.", null=True)),
                ('external_audience', models.BooleanField(help_text='Specify if the application is used by people outside the organization.', default=False)),
                ('internet_accessible', models.BooleanField(help_text='Specify if the application is accessible from the public internet.', default=False)),
                ('override_dcl', models.IntegerField(blank=True, choices=[(None, 'Not Specified'), (1, 'DCL 1'), (2, 'DCL 2'), (3, 'DCL 3'), (4, 'DCL 4')], help_text='Overrides the calculated data classification level.', null=True)),
                ('override_reason', models.TextField(blank=True, help_text='Specify why the calculated data classification level is being overridden.')),
                ('threadfix_organization_id', models.PositiveIntegerField(null=True, blank=True)),
                ('threadfix_application_id', models.PositiveIntegerField(null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'get_latest_by': 'modified_date',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApplicationFileUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('file', models.FileField(upload_to='')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('file_type', models.IntegerField(choices=[(1, 'Report'), (2, 'Documentation')])),
                ('application', models.ForeignKey(to='boh.Application')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('description', models.TextField(blank=True)),
                ('category', models.CharField(max_length=10, choices=[('global', 'Global'), ('personal', 'Personal'), ('company', 'Company'), ('student', 'Student'), ('government', 'Government'), ('pci', 'Payment Card Industry'), ('medical', 'Medical')])),
                ('weight', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Engagement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('status', models.CharField(max_length=7, default='pending', choices=[('pending', 'Pending'), ('open', 'Open'), ('closed', 'Closed')])),
                ('start_date', models.DateField(help_text='The date the engagement is scheduled to begin.')),
                ('end_date', models.DateField(help_text='The date the engagement is scheduled to complete.')),
                ('description', models.TextField(blank=True)),
                ('open_date', models.DateTimeField(blank=True, help_text='The date and time when the status is changed to open.', null=True)),
                ('close_date', models.DateTimeField(blank=True, help_text='The date and time when the status is changed to closed.', null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('application', models.ForeignKey(to='boh.Application')),
            ],
            options={
                'ordering': ['start_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EngagementComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('message', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('engagement', models.ForeignKey(to='boh.Engagement')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('environment_type', models.CharField(max_length=4, help_text='Specify the type of environment.', choices=[('dev', 'Development'), ('int', 'Integration'), ('qa', 'Quality Assurance'), ('ppe', 'Pre-Production'), ('cat', 'Customer Acceptance'), ('prod', 'Production')])),
                ('description', models.TextField(blank=True, help_text="Information about the environment's purpose, physical location, hardware, and deployment.")),
                ('testing_approved', models.BooleanField(help_text='Specify if security testing has been approved for this environment.', default=False)),
                ('application', models.ForeignKey(to='boh.Application')),
            ],
            options={
                'ordering': ['-testing_approved', 'environment_type'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnvironmentCredentials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('username', models.CharField(max_length=128, blank=True)),
                ('password', models.CharField(max_length=128, blank=True)),
                ('role_description', models.CharField(max_length=128, blank=True, help_text="A brief description of the user's role or permissions. (e.g., Guest, Admin)")),
                ('notes', models.TextField(blank=True, help_text='Additional information about these credentials.')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('environment', models.ForeignKey(to='boh.Environment')),
            ],
            options={
                'verbose_name_plural': 'Environment credentials',
                'ordering': ['username', 'password'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnvironmentLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('location', models.URLField(help_text='A URL for the environment. (e.g., http://www.google.com/, https://www.owasp.org/)')),
                ('notes', models.TextField(blank=True, help_text="Information about the location's purpose, physical location, and deployment.")),
                ('environment', models.ForeignKey(to='boh.Environment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32, help_text='A unique name for the organization.', unique=True)),
                ('description', models.TextField(blank=True, help_text="Information about the organization's purpose, history, and structure.")),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=75)),
                ('phone_work', models.CharField(max_length=15, blank=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('phone_mobile', models.CharField(max_length=15, blank=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('job_title', models.CharField(max_length=128, blank=True)),
                ('role', models.CharField(max_length=17, choices=[('developer', 'Developer'), ('qa', 'Quality Assurance'), ('operations', 'Operations'), ('manager', 'Manager'), ('security officer', 'Security Officer'), ('security champion', 'Security Champion')])),
            ],
            options={
                'verbose_name_plural': 'People',
                'ordering': ['last_name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('owner', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('application', models.ForeignKey(to='boh.Application')),
                ('person', models.ForeignKey(to='boh.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('color', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(message="Color must be entered in the 6 characters hex format. (e.g., 'd94d59')", regex='^[0-9A-Fa-f]{6}$')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ThreadFix',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32, help_text='A unique name describing the ThreadFix server.', unique=True)),
                ('host', models.URLField(help_text='The URL for the ThreadFix server. (e.g., http://localhost:8080/threadfix/)')),
                ('api_key', models.CharField(max_length=50, help_text='The API key can be generated on the ThreadFix API Key page.')),
            ],
            options={
                'verbose_name': 'ThreadFix',
                'verbose_name_plural': 'ThreadFix',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='relation',
            unique_together=set([('person', 'application')]),
        ),
        migrations.AddField(
            model_name='organization',
            name='people',
            field=models.ManyToManyField(to='boh.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='engagement',
            name='requestor',
            field=models.ForeignKey(to='boh.Person', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='data_elements',
            field=models.ManyToManyField(null=True, blank=True, to='boh.DataElement'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='organization',
            field=models.ForeignKey(to='boh.Organization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='people',
            field=models.ManyToManyField(to='boh.Person', through='boh.Relation', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='tags',
            field=models.ManyToManyField(to='boh.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='threadfix',
            field=models.ForeignKey(to='boh.ThreadFix', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_type',
            field=models.ForeignKey(to='boh.ActivityType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='engagement',
            field=models.ForeignKey(to='boh.Engagement'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]

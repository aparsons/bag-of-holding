from datetime import date, timedelta
import uuid

import phonenumbers

from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import ugettext as _

from .behaviors import TimeStampedModel
from . import helpers, managers


class Tag(models.Model):
    """Associated with application for search and categorization."""

    color_regex = RegexValidator(regex=r'^[0-9A-Fa-f]{6}$', message="Color must be entered in the 6 character hex format.")

    name = models.CharField(max_length=64, unique=True, help_text='A unique name for this tag.')
    color = models.CharField(max_length=6, validators=[color_regex], help_text='Specify a 6 character hex color value. (e.g., \'d94d59\')')

    description = models.CharField(max_length=64, blank=True, help_text='A short description of this tag\'s purpose to be shown in tooltips.')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.color = self.color.lower()  # Convert color to lowercase
        super(Tag, self).save(*args, **kwargs)


class Person(models.Model):
    """Information about a person."""

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    DEVELOPER_ROLE = 'developer'
    QUALITY_ASSURANCE_ROLE = 'qa'
    OPERATIONS_ROLE = 'operations'
    MANAGER_ROLE = 'manager'
    SECURITY_OFFICER_ROLE = 'security officer'
    SECURITY_CHAMPION_ROLE = 'security champion'
    ROLE_CHOICES = (
        (DEVELOPER_ROLE, 'Developer'),
        (QUALITY_ASSURANCE_ROLE, 'Quality Assurance'),
        (OPERATIONS_ROLE, 'Operations'),
        (MANAGER_ROLE, 'Manager'),
        (SECURITY_OFFICER_ROLE, 'Security Officer'),
        (SECURITY_CHAMPION_ROLE, 'Security Champion'),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=128, unique=True)
    role = models.CharField(max_length=17, choices=ROLE_CHOICES)
    phone_work = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    phone_mobile = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    job_title = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ['last_name']
        verbose_name_plural = 'People'

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        if self.phone_work:
            self.phone_work = phonenumbers.format_number(phonenumbers.parse(self.phone_work, 'US'), phonenumbers.PhoneNumberFormat.E164)
        if self.phone_mobile:
            self.phone_mobile = phonenumbers.format_number(phonenumbers.parse(self.phone_mobile, 'US'), phonenumbers.PhoneNumberFormat.E164)
        self.email = self.email.lower()
        super(Person, self).save(*args, **kwargs)


class Organization(models.Model):
    """Entities under which applications belong."""

    name = models.CharField(max_length=32, unique=True, help_text='A unique name for the organization.')
    description = models.TextField(blank=True, help_text='Information about the organization\'s purpose, history, and structure.')

    people = models.ManyToManyField(Person, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class DataElement(models.Model):
    """An individual data element stored within an application. Used for data classification."""

    GLOBAL_CATEGORY = 'global'
    PERSONAL_CATEGORY = 'personal'
    COMPANY_CATEGORY = 'company'
    STUDENT_CATEGORY = 'student'
    GOVERNMENT_CATEGORY = 'government'
    PCI_CATEGORY = 'pci'
    MEDICAL_CATEGORY = 'medical'
    CATEGORY_CHOICES = (
        (GLOBAL_CATEGORY, 'Global'),
        (PERSONAL_CATEGORY, 'Personal'),
        (COMPANY_CATEGORY, 'Company'),
        (STUDENT_CATEGORY, 'Student'),
        (GOVERNMENT_CATEGORY, 'Government'),
        (PCI_CATEGORY, 'Payment Card Industry'),
        (MEDICAL_CATEGORY, 'Medical'),
    )

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    weight = models.PositiveIntegerField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Technology(models.Model):
    """Architectural details for an application."""
    PROGRAMMING_LANGUAGE_CATEGORY = 'language'
    OPERATING_SYSTEM_CATEGORY = 'operating system'
    DATA_STORE_CATEGORY = 'data store'
    FRAMEWORK_CATEGORY = 'framework'
    THIRD_PARTY_COMPONENT = 'third-party component'
    WEB_SERVER_CATEGORY = 'web server'
    APPLICATION_SERVER_CATEGORY = 'application server'
    HOSTING_PROVIDER_CATEGORY = 'hosting provider'
    DENIAL_OF_SERVICE_CATEGORY = 'denial of service'
    FIREWALL_CATEGORY = 'firewall'
    CATEGORY_CHOICES = (
        (PROGRAMMING_LANGUAGE_CATEGORY, 'Language'),
        (OPERATING_SYSTEM_CATEGORY, 'Operating System'),
        (DATA_STORE_CATEGORY, 'Data Store'),
        (FRAMEWORK_CATEGORY, 'Framework'),
        (THIRD_PARTY_COMPONENT, 'Third-Party Component'),
        (APPLICATION_SERVER_CATEGORY, 'Application Server'),
        (WEB_SERVER_CATEGORY, 'Web Server'),
        (HOSTING_PROVIDER_CATEGORY, 'Hosting Provider'),
        (DENIAL_OF_SERVICE_CATEGORY, 'DDoS Protection'),
        (FIREWALL_CATEGORY, 'Firewall'),
    )

    name = models.CharField(max_length=64, help_text='The name of the technology.')
    category = models.CharField(max_length=21, choices=CATEGORY_CHOICES, help_text='The type of technology.')
    description = models.CharField(max_length=256, blank=True, help_text='Information about the technology.')
    reference = models.URLField(blank=True, help_text='An external URL for more information.')

    class Meta:
        ordering = ['category', 'name']
        verbose_name_plural = 'Technologies'

    def __str__(self):
        return self.get_category_display() + ' :: ' + self.name


class Regulation(models.Model):
    """Regulations applicable to applications."""
    PRIVACY_CATEGORY = 'privacy'
    FINANCE_CATEGORY = 'finance'
    EDUCATION_CATEGORY = 'education'
    MEDICAL_CATEGORY = 'medical'
    OTHER_CATEGORY = 'other'
    CATEGORY_CHOICES = (
        (PRIVACY_CATEGORY, 'Privacy'),
        (FINANCE_CATEGORY, 'Finance'),
        (EDUCATION_CATEGORY, 'Education'),
        (MEDICAL_CATEGORY, 'Medical'),
        (OTHER_CATEGORY, 'Other'),
    )

    name = models.CharField(max_length=128, help_text='The name of the legislation.')
    acronym = models.CharField(max_length=20, unique=True, help_text='A shortened representation of the name.')
    category = models.CharField(max_length=9, choices=CATEGORY_CHOICES, help_text='The subject of the regulation.')
    jurisdiction = models.CharField(max_length=64, help_text='The territory over which the regulation applies.')
    description = models.TextField(blank=True, help_text='Information about the regulation\'s purpose.')
    reference = models.URLField(blank=True, help_text='An external URL for more information.')

    class Meta:
        ordering = ['jurisdiction', 'category', 'name']

    def __str__(self):
        return self.acronym + ' (' + self.jurisdiction + ')'


class ServiceLevelAgreement(models.Model):
    """Service Level Agreements to be applied to applications."""
    name = models.CharField(max_length=64, help_text='The name of the service level agreement.')
    description = models.CharField(max_length=256, blank=True, help_text='Information about this service level agreement\'s scope, quality, and responsibilities.')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ThreadFix(models.Model):
    """ThreadFix server connection information."""

    name = models.CharField(max_length=32, unique=True, help_text='A unique name describing the ThreadFix service.')
    host = models.URLField(help_text='The URL for the ThreadFix server. (e.g., http://localhost:8080/threadfix/)')
    api_key = models.CharField(max_length=50, help_text='The API key can be generated on the ThreadFix API Key page.')  # https://github.com/denimgroup/threadfix/blob/dev/threadfix-main/src/main/java/com/denimgroup/threadfix/service/APIKeyServiceImpl.java#L103
    verify_ssl = models.BooleanField(default=True, help_text='Specify if API requests will verify the host\'s SSL certificate. If disabled, API requests could be intercepted by third-parties.')

    class Meta:
        verbose_name = 'ThreadFix'
        verbose_name_plural = 'ThreadFix'

    def __str__(self):
        return self.name + ' - ' + self.host


class Application(TimeStampedModel, models.Model):
    """Contains information about a software application."""

    WEB_PLATFORM = 'web'
    DESKTOP_PLATFORM = 'desktop'
    MOBILE_PLATFORM = 'mobile'
    WEB_SERVICE_PLATFORM = 'web service'
    PLATFORM_CHOICES = (
        (WEB_PLATFORM, 'Web'),
        (DESKTOP_PLATFORM, 'Desktop'),
        (MOBILE_PLATFORM, 'Mobile'),
        (WEB_SERVICE_PLATFORM, 'Web Service'),
    )

    IDEA_LIFECYCLE = 'idea'
    EXPLORE_LIFECYCLE = 'explore'
    VALIDATE_LIFECYCLE = 'validate'
    GROW_LIFECYCLE = 'grow'
    SUSTAIN_LIFECYCLE = 'sustain'
    RETIRE_LIFECYCLE = 'retire'
    LIFECYCLE_CHOICES = (
        (IDEA_LIFECYCLE, 'Idea'),
        (EXPLORE_LIFECYCLE, 'Explore'),
        (VALIDATE_LIFECYCLE, 'Validate'),
        (GROW_LIFECYCLE, 'Grow'),
        (SUSTAIN_LIFECYCLE, 'Sustain'),
        (RETIRE_LIFECYCLE, 'Retire'),
    )

    THIRD_PARTY_LIBRARY_ORIGIN = 'third party library'
    PURCHASED_ORIGIN = 'purchased'
    CONTRACTOR_ORIGIN = 'contractor'
    INTERNALLY_DEVELOPED_ORIGIN = 'internal'
    OPEN_SOURCE_ORIGIN = 'open source'
    OUTSOURCED_ORIGIN = 'outsourced'
    ORIGIN_CHOICES = (
        (THIRD_PARTY_LIBRARY_ORIGIN, 'Third Party Library'),
        (PURCHASED_ORIGIN, 'Purchased'),
        (CONTRACTOR_ORIGIN, 'Contractor Developed'),
        (INTERNALLY_DEVELOPED_ORIGIN, 'Internally Developed'),
        (OPEN_SOURCE_ORIGIN, 'Open Source'),
        (OUTSOURCED_ORIGIN, 'Outsourced'),
    )

    VERY_HIGH_CRITICALITY = 'very high'
    HIGH_CRITICALITY = 'high'
    MEDIUM_CRITICALITY = 'medium'
    LOW_CRITICALITY = 'low'
    VERY_LOW_CRITICALITY = 'very low'
    NONE_CRITICALITY = 'none'
    BUSINESS_CRITICALITY_CHOICES = (
        (VERY_HIGH_CRITICALITY, 'Very High'),
        (HIGH_CRITICALITY, 'High'),
        (MEDIUM_CRITICALITY, 'Medium'),
        (LOW_CRITICALITY, 'Low'),
        (VERY_LOW_CRITICALITY, 'Very Low'),
        (NONE_CRITICALITY, 'None'),
    )

    DCL_1 = 1
    DCL_2 = 2
    DCL_3 = 3
    DCL_4 = 4
    DATA_CLASSIFICATION_CHOICES = (
        (None, 'Not Specified'),
        (DCL_1, 'DCL 1'),
        (DCL_2, 'DCL 2'),
        (DCL_3, 'DCL 3'),
        (DCL_4, 'DCL 4'),
    )

    ASVS_0 = 0
    ASVS_1 = 1
    ASVS_2 = 2
    ASVS_3 = 3
    ASVS_CHOICES = (
        (None, 'Not Specified'),
        (ASVS_0, '0'),
        (ASVS_1, '1'),
        (ASVS_2, '2'),
        (ASVS_3, '3'),
    )

    # General
    name = models.CharField(max_length=128, unique=True, help_text='A unique name for the application.')
    description = models.TextField(blank=True, help_text='Information about the application\'s purpose, history, and design.')

    # Metadata
    business_criticality = models.CharField(max_length=9, choices=BUSINESS_CRITICALITY_CHOICES, blank=True, null=True)
    platform = models.CharField(max_length=11, choices=PLATFORM_CHOICES, blank=True, null=True)
    lifecycle = models.CharField(max_length=8, choices=LIFECYCLE_CHOICES, blank=True, null=True)
    origin = models.CharField(max_length=19, choices=ORIGIN_CHOICES, blank=True, null=True)
    user_records = models.PositiveIntegerField(blank=True, null=True, help_text='Estimate the number of user records within the application.')
    revenue = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, help_text='Estimate the application\'s revenue in USD.')
    external_audience = models.BooleanField(default=False, help_text='Specify if the application is used by people outside the organization.')
    internet_accessible = models.BooleanField(default=False, help_text='Specify if the application is accessible from the public internet.')
    requestable = models.NullBooleanField(default=True, help_text=_('Specify if activities can be externally requested for this application.'))

    technologies = models.ManyToManyField(Technology, blank=True)
    regulations = models.ManyToManyField(Regulation, blank=True)
    service_level_agreements = models.ManyToManyField(ServiceLevelAgreement, blank=True)

    # Data Classification
    # TODO Move to Data Classification Benchmark
    data_elements = models.ManyToManyField(DataElement, blank=True)
    override_dcl = models.IntegerField(choices=DATA_CLASSIFICATION_CHOICES, blank=True, null=True, help_text='Overrides the calculated data classification level.')
    override_reason = models.TextField(blank=True, help_text='Specify why the calculated data classification level is being overridden.')

    # ThreadFix
    threadfix = models.ForeignKey(ThreadFix, blank=True, null=True, help_text='The ThreadFix service to connect to this application.')
    threadfix_team_id = models.PositiveIntegerField(blank=True, null=True, help_text='The unique team identifier used within ThreadFix.')
    threadfix_application_id = models.PositiveIntegerField(blank=True, null=True, help_text='The unique application identifier used within ThreadFix.')

    # OWASP
    # TODO Move to OWASP ASVS Benchmark
    asvs_level = models.IntegerField(choices=ASVS_CHOICES,blank=True, null=True, help_text='Assessed ASVS Level')
    asvs_level_percent_achieved = models.PositiveIntegerField(blank=True, null=True, help_text='Percent compliant to the targeted ASVS level.')
    asvs_doc_url = models.URLField(blank=True, help_text='URL to the detailed ASVS assessment.')
    asvs_level_target = models.IntegerField(choices=ASVS_CHOICES,blank=True, null=True, help_text='Targeted ASVS level for this application.')

    # Misc

    """
    source code repo
    bug tracking tool
    developer experience / familiarity
    programming language/s
    id for whitehat + checkmarx (third-party ids)
    password policy
    """

    organization = models.ForeignKey(Organization, help_text='The organization containing this application.')
    people = models.ManyToManyField(Person, through='Relation', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    objects = managers.ApplicationManager.from_queryset(managers.ApplicationQuerySet)()

    class Meta:
        get_latest_by = 'modified_date'
        ordering = ['name']

    def __str__(self):
        return self.name

    def data_classification_level(self):
        """Returns the data classification level of the selected data elements."""
        return helpers.data_classification_level(self.data_sensitivity_value())

    def data_sensitivity_value(self):
        """Returns the calculated data sensitivity value of the selected data elements."""
        return helpers.data_sensitivity_value(self.data_elements.all())

    def is_new(self):
        """Returns true if the application was created in the last 7 days"""
        delta = self.created_date - timezone.now()
        return delta >= timedelta(days=-7)


class ThreadFixMetrics(TimeStampedModel, models.Model):
    """Point in time metrics from ThreadFix for an application."""

    critical_count = models.PositiveIntegerField(default=0)
    high_count = models.PositiveIntegerField(default=0)
    medium_count = models.PositiveIntegerField(default=0)
    low_count = models.PositiveIntegerField(default=0)
    informational_count = models.PositiveIntegerField(default=0)

    application = models.ForeignKey(Application)

    class Meta:
        get_latest_by = 'created_date'
        verbose_name = 'ThreadFix metrics'
        verbose_name_plural = 'ThreadFix metrics'

    def total(self):
        return self.critical_count + self.high_count + self.medium_count + self.low_count + self.informational_count


class Relation(models.Model):
    """Associates a person with an application with a role."""

    owner = models.BooleanField(default=False, help_text='Specify if this person is an application owner.')
    emergency = models.BooleanField(default=False, help_text='Specify if this person is an emergency contact.')
    notes = models.TextField(blank=True, help_text='Any notes about this person\'s connection to the application.')

    person = models.ForeignKey(Person, help_text='The person associated with the application.')
    application = models.ForeignKey(Application)

    class Meta:
        unique_together = ('person', 'application')

    def __str__(self):
        return self.person.first_name + ' ' + self.person.last_name + ' - ' + self.application.name


class Environment(models.Model):
    """Container for information about a web server environment."""

    DEVELOPMENT_ENVIRONMENT = 'dev'
    INTEGRATION_ENVIRONMENT = 'int'
    QUALITY_ASSURANCE_ENVIRONMENT = 'qa'
    PRE_PRODUCTION_ENVIRONMENT = 'ppe'
    CUSTOMER_ACCEPTANCE_ENVIRONMENT = 'cat'
    PRODUCTION_ENVIRONMENT = 'prod'
    ENVIRONMENT_CHOICES = (
        (DEVELOPMENT_ENVIRONMENT, 'Development'),
        (INTEGRATION_ENVIRONMENT, 'Integration'),
        (QUALITY_ASSURANCE_ENVIRONMENT, 'Quality Assurance'),
        (PRE_PRODUCTION_ENVIRONMENT, 'Pre-Production'),
        (CUSTOMER_ACCEPTANCE_ENVIRONMENT, 'Customer Acceptance'),
        (PRODUCTION_ENVIRONMENT, 'Production'),
    )

    environment_type = models.CharField(max_length=4, choices=ENVIRONMENT_CHOICES, help_text='Specify the type of environment.')
    description = models.TextField(blank=True, help_text='Information about the environment\'s purpose, physical location, hardware, and deployment.')
    testing_approved = models.BooleanField(default=False, help_text='Specify if security testing has been approved for this environment.')

    application = models.ForeignKey(Application)

    class Meta:
        ordering = ['-testing_approved', 'environment_type']

    def __str__(self):
        return self.application.name + ' (' + dict(Environment.ENVIRONMENT_CHOICES)[self.environment_type] + ')'


class EnvironmentLocation(models.Model):
    """URL for a specific environment"""

    location = models.URLField(help_text='A URL for the environment. (e.g., http://www.google.com/, https://www.owasp.org/)')
    notes = models.TextField(blank=True, help_text='Information about the location\'s purpose, physical location, and deployment.')

    environment = models.ForeignKey(Environment)

    def __str__(self):
        return self.location


class EnvironmentCredentials(TimeStampedModel, models.Model):
    """Credentials for a specific environment."""

    username = models.CharField(max_length=128, blank=True)
    password = models.CharField(max_length=128, blank=True)
    role_description = models.CharField(max_length=128, blank=True, help_text='A brief description of the user\'s role or permissions. (e.g., Guest, Admin)')
    notes = models.TextField(blank=True, help_text='Additional information about these credentials.')

    environment = models.ForeignKey(Environment)

    class Meta:
        verbose_name_plural = 'Environment credentials'
        ordering = ['username', 'password']


class Engagement(TimeStampedModel, models.Model):
    """Container for activities performed for an application over a duration."""

    PENDING_STATUS = 'pending'
    OPEN_STATUS = 'open'
    CLOSED_STATUS = 'closed'
    STATUS_CHOICES = (
        (PENDING_STATUS, 'Pending'),
        (OPEN_STATUS, 'Open'),
        (CLOSED_STATUS, 'Closed')
    )

    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default=PENDING_STATUS)
    start_date = models.DateField(help_text='The date the engagement is scheduled to begin.')
    end_date = models.DateField(help_text='The date the engagement is scheduled to complete.')
    description = models.TextField(blank=True)

    open_date = models.DateTimeField(blank=True, null=True, help_text='The date and time when the status is changed to open.')
    close_date = models.DateTimeField(blank=True, null=True, help_text='The date and time when the status is changed to closed.')
    duration = models.DurationField(blank=True, null=True)

    requestor = models.ForeignKey(Person, blank=True, null=True, help_text='Specify who requested this engagement.')
    application = models.ForeignKey(Application)

    objects = managers.EngagementManager.from_queryset(managers.EngagementQuerySet)()
    metrics = managers.EngagementMetrics.from_queryset(managers.EngagementQuerySet)()

    class Meta:
        get_latest_by = 'close_date'
        ordering = ['start_date']

    def save(self, *args, **kwargs):
        """Automatically sets the open and closed dates when the status changes."""
        if self.pk is not None:
            engagement = Engagement.objects.get(pk=self.pk)
            now = timezone.now()
            if engagement.status != self.status:
                if self.status == Engagement.PENDING_STATUS:
                    self.open_date = None
                    self.close_date = None
                elif self.status == Engagement.OPEN_STATUS:
                    self.open_date = now
                    self.close_date = None
                elif self.status == Engagement.CLOSED_STATUS:
                    if self.open_date is None:
                        self.open_date = now
                    self.close_date = now

        if self.open_date is not None and self.close_date is not None:
            self.duration = self.close_date - self.open_date
        super(Engagement, self).save(*args, **kwargs)

    def is_pending(self):
        return self.status == Engagement.PENDING_STATUS

    def is_open(self):
        return self.status == Engagement.OPEN_STATUS

    def is_closed(self):
        return self.status == Engagement.CLOSED_STATUS

    def is_ready_for_work(self):
        """If the engagement is pending on or after the start date."""
        if self.status == Engagement.PENDING_STATUS:
            if date.today() >= self.start_date:
                return True
        return False

    def is_past_due(self):
        """If the engagement is not closed by the end date."""
        if self.status == Engagement.PENDING_STATUS or self.status == Engagement.OPEN_STATUS:
            if date.today() > self.end_date:
                return True
        return False


class ActivityType(TimeStampedModel, models.Model):
    """Types of work."""

    name = models.CharField(max_length=128, unique=True, help_text=_('A unique name for this activity type.'))
    documentation = models.TextField(blank=True, help_text=_('Guidelines, procedures, and techniques for this activity type.'))

    objects = managers.ActivityTypeManager.from_queryset(managers.ActivityTypeQuerySet)()
    metrics = managers.ActivityTypeMetrics.from_queryset(managers.ActivityTypeQuerySet)()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Activity(models.Model):
    """A unit of work performed for an application over a duration."""

    PENDING_STATUS = 'pending'
    OPEN_STATUS = 'open'
    CLOSED_STATUS = 'closed'
    STATUS_CHOICES = (
        (PENDING_STATUS, 'Pending'),
        (OPEN_STATUS, 'Open'),
        (CLOSED_STATUS, 'Closed')
    )

    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default=PENDING_STATUS)
    description = models.TextField(blank=True)
    open_date = models.DateTimeField(blank=True, null=True, help_text='The date and time when the status is changed to open.')
    close_date = models.DateTimeField(blank=True, null=True, help_text='The date and time when the status is changed to closed.')
    duration = models.DurationField(blank=True, null=True)

    activity_type = models.ForeignKey(ActivityType)
    engagement = models.ForeignKey(Engagement)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    objects = managers.ActivityManager.from_queryset(managers.ActivityQuerySet)()

    class Meta:
        ordering = ['engagement__start_date']
        verbose_name_plural = 'Activities'

    def __str__(self):
        return self.activity_type.name

    def save(self, *args, **kwargs):
        """
        Automatically sets the open and closed dates when the status changes.
        Opens parent engagement if child activity is opened.
        Closes parent engagement if all child activities are closed.
        """
        if self.pk is not None:
            activity = Activity.objects.get(pk=self.pk)
            if activity.status != self.status:  # When status changed
                now = timezone.now()
                if self.status == Activity.PENDING_STATUS:
                    self.open_date = None
                    self.close_date = None
                elif self.status == Activity.OPEN_STATUS:
                    self.open_date = now
                    self.close_date = None

                    # Open the parent engagement if the activity is opened
                    if self.engagement.status is not Engagement.OPEN_STATUS:
                        self.engagement.status = Engagement.OPEN_STATUS
                        self.engagement.save()
                elif self.status == Activity.CLOSED_STATUS:
                    if self.open_date is None:
                        self.open_date = now
                    self.close_date = now

                    # If all of the parent engagement activities are closed, close the parent engagement
                    close = True
                    for current_activity in self.engagement.activity_set.exclude(id=self.id):
                        if current_activity.status != Activity.CLOSED_STATUS:
                            close = False
                            break
                    if close:
                        self.engagement.status = Engagement.CLOSED_STATUS
                        self.engagement.save()
        if self.open_date is not None and self.close_date is not None:
            self.duration = self.close_date - self.open_date
        super(Activity, self).save(*args, **kwargs)

    def is_pending(self):
        return self.status == Activity.PENDING_STATUS

    def is_open(self):
        return self.status == Activity.OPEN_STATUS

    def is_closed(self):
        return self.status == Activity.CLOSED_STATUS

    def is_ready_for_work(self):
        """If the activity is pending on or after the parent engagement's start date."""
        if self.status == Activity.PENDING_STATUS:
            if date.today() >= self.engagement.start_date:
                return True
        return False

    def is_past_due(self):
        """If the activity is not closed by the parent engagement's end date."""
        if self.status == Activity.PENDING_STATUS or self.status == Activity.OPEN_STATUS:
            if date.today() > self.engagement.end_date:
                return True
        return False


class Comment(TimeStampedModel, models.Model):
    """Abstract message about an engagement or activity."""

    message = models.TextField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.message

    class Meta:
        abstract = True


class EngagementComment(Comment):
    """Comment for a specific engagement."""

    engagement = models.ForeignKey(Engagement)


class ActivityComment(Comment):
    """Comment for a specific activity."""

    activity = models.ForeignKey(Activity)


class ExternalRequest(TimeStampedModel, models.Model):
    """An external request for engagement."""

    token = models.UUIDField(default=uuid.uuid4, editable=False)

    requestor = models.ForeignKey(Person)
    application = models.ForeignKey(Application, blank=True)
    activities = models.ManyToManyField(ActivityType, limit_choices_to={'requestable': True})
    # Application FK
    # Person FK (Can be blank)
    # Requested Activities (Multiple)
    # Status Page UUID
    # Created Engagement (blank)

    # Some sort of accept/decline/other status


class FileUpload(TimeStampedModel, models.Model):
    """Abstract file upload by a user."""

    file = models.FileField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True


class ApplicationFileUpload(FileUpload):
    """A file uploaded associated with an application."""

    REPORT_FILE_TYPE = 'report'
    DOCUMENTATION_FILE_TYPE = 'documentation'
    FILE_TYPE_CHOICES = (
        (REPORT_FILE_TYPE, 'Report'),
        (DOCUMENTATION_FILE_TYPE, 'Documentation'),
    )

    # Draft boolean field

    file_type = models.CharField(max_length=13, choices=FILE_TYPE_CHOICES)

    application = models.ForeignKey(Application)

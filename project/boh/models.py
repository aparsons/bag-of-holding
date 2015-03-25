from datetime import date, timedelta

import phonenumbers

from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


class Tag(models.Model):
    """Associated with application for search and catagorization."""

    color_regex = RegexValidator(regex=r'^[0-9A-Fa-f]{6}$', message="Color must be entered in the 6 character hex format.")

    name = models.CharField(max_length=64, unique=True, help_text='A unique name for this tag.')
    description = models.CharField(max_length=64, blank=True, help_text='A short description of this tag\'s purpose to be shown in tooltips.')
    color = models.CharField(max_length=6, validators=[color_regex], help_text='Specify a 6 character hex color value. (e.g., \'d94d59\')')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.color = self.color.lower() # Convert color to lowercase
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
    email = models.EmailField(unique=True)
    phone_work = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    phone_mobile = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    job_title = models.CharField(max_length=128, blank=True)
    role = models.CharField(max_length=17, choices=ROLE_CHOICES)

    class Meta:
        ordering = ['last_name']
        verbose_name_plural = 'People'

    def __str__(self):
        return self.last_name + ', ' + self.first_name

    def save(self, *args, **kwargs):
        if self.phone_work:
            self.phone_work = phonenumbers.format_number(phonenumbers.parse(self.phone_work, 'US'), phonenumbers.PhoneNumberFormat.E164)
        if self.phone_mobile:
            self.phone_mobile = phonenumbers.format_number(phonenumbers.parse(self.phone_mobile, 'US'), phonenumbers.PhoneNumberFormat.E164)
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


class ThreadFix(models.Model):
    """ThreadFix server connection information."""

    name = models.CharField(max_length=32, unique=True, help_text='A unique name describing the ThreadFix service.')
    host = models.URLField(help_text='The URL for the ThreadFix server. (e.g., http://localhost:8080/threadfix/)')
    api_key = models.CharField(max_length=50, help_text='The API key can be generated on the ThreadFix API Key page.') # https://github.com/denimgroup/threadfix/blob/dev/threadfix-main/src/main/java/com/denimgroup/threadfix/service/APIKeyServiceImpl.java#L103
    verify_ssl = models.BooleanField(default=True, help_text='Specify if API requests will verify the host\'s SSL certificate. If disabled, API requests could be intercepted by third-parties.')

    class Meta:
        verbose_name = "ThreadFix"
        verbose_name_plural = 'ThreadFix'

    def __str__(self):
        return self.name + ' - ' + self.host


class Application(models.Model):
    """Contains infomation about a software application."""

    WEB_PLATFORM = 'web'
    DESKTOP_PLATFORM = 'desktop'
    MOBILE_PLATFORM = 'mobile'
    WEB_SERVICE_PLATFORM = 'web service'
    PLATFORM_CHOICES = (
        (None, 'Not Specified'),
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
        (None, 'Not Specified'),
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
        (None, 'Not Specified'),
        (THIRD_PARTY_LIBRARY_ORIGIN, 'Third Party Library'),
        (PURCHASED_ORIGIN, 'Purchased'),
        (CONTRACTOR_ORIGIN, 'Contractor'),
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
        (None, 'Not Specified'),
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

    # General
    name = models.CharField(max_length=128, unique=True, help_text='A unique name for the application.')
    description = models.TextField(blank=True, help_text='Information about the application\'s purpose, history, and design.')

    # Metadata
    platform = models.CharField(max_length=11, choices=PLATFORM_CHOICES, blank=True, null=True)
    lifecycle = models.CharField(max_length=8, choices=LIFECYCLE_CHOICES, blank=True, null=True)
    origin = models.CharField(max_length=19, choices=ORIGIN_CHOICES, blank=True, null=True)
    business_criticality = models.CharField(max_length=9, choices=BUSINESS_CRITICALITY_CHOICES, blank=True, null=True)
    user_records = models.PositiveIntegerField(blank=True, null=True, help_text='Estimate the number of user records within the application.')
    revenue = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, help_text='Estimate the application\'s revenue in USD.')
    external_audience = models.BooleanField(default=False, help_text='Specify if the application is used by people outside the organization.')
    internet_accessible = models.BooleanField(default=False, help_text='Specify if the application is accessible from the public internet.')

    # Data Classification
    data_elements = models.ManyToManyField(DataElement, blank=True, null=True)
    override_dcl = models.IntegerField(choices=DATA_CLASSIFICATION_CHOICES, blank=True, null=True, help_text='Overrides the calculated data classification level.')
    override_reason = models.TextField(blank=True, help_text='Specify why the calculated data classification level is being overridden.')

    # ThreadFix
    threadfix = models.ForeignKey(ThreadFix, blank=True, null=True)
    threadfix_team_id = models.PositiveIntegerField(blank=True, null=True)
    threadfix_application_id = models.PositiveIntegerField(blank=True, null=True)

    # Misc
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    #source code repo
    #bug tracking tool
    #developer experience / familiarity
    #programming language/s
    #id for whitehat + checkmarx (third-party ids)
    #password policy

    organization = models.ForeignKey(Organization, help_text='The organization containing this application.')
    people = models.ManyToManyField(Person, through='Relation', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        get_latest_by = "modified_date"
        ordering = ['name']

    def data_classification_level(self):
        dsv = self.data_sensitivity_value()
        if dsv < 15:
            return Application.DCL_1
        elif dsv >= 15 and dsv < 100:
            return Application.DCL_2
        elif dsv >= 100 and dsv < 150:
            return Application.DCL_3
        else:
            return Application.DCL_4

    def data_sensitivity_value(self):
        """
        Calculates the data sensitivity value.
        DSV = Global * (Personal + Student + Government) + PCI + Health + Company
        """
        vector = {
            DataElement.GLOBAL_CATEGORY: 1.0,
            DataElement.PERSONAL_CATEGORY: 0.0,
            DataElement.COMPANY_CATEGORY: 0.0,
            DataElement.STUDENT_CATEGORY: 0.0,
            DataElement.GOVERNMENT_CATEGORY: 0.0,
            DataElement.PCI_CATEGORY: 0.0,
            DataElement.MEDICAL_CATEGORY: 0.0,
        }

        for data_element in self.data_elements.all():
            vector[data_element.category] += data_element.weight

        dsv = vector[DataElement.GLOBAL_CATEGORY] * (vector[DataElement.PERSONAL_CATEGORY] + vector[DataElement.STUDENT_CATEGORY] + vector[DataElement.GOVERNMENT_CATEGORY]) + vector[DataElement.PCI_CATEGORY] + vector[DataElement.MEDICAL_CATEGORY] + vector[DataElement.COMPANY_CATEGORY]

        #if dsv > 200:
        #    dsv = 200

        return dsv

    def is_new(self):
        """Returns true if the application was created in the last 7 days"""
        delta = self.created_date - timezone.now()
        return delta >= timedelta(days=-7)


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
        return self.application.name + ' ' + dict(Environment.ENVIRONMENT_CHOICES)[self.environment_type]


class EnvironmentLocation(models.Model):
    """URL for a specific environment"""

    location = models.URLField(help_text='A URL for the environment. (e.g., http://www.google.com/, https://www.owasp.org/)')
    notes = models.TextField(blank=True, help_text='Information about the location\'s purpose, physical location, and deployment.')

    environment = models.ForeignKey(Environment)

    def __str__(self):
        return self.location


class EnvironmentCredentials(models.Model):
    """Credentials for a specific environment."""

    username = models.CharField(max_length=128, blank=True) # Needs to be encrypted
    password = models.CharField(max_length=128, blank=True) # Needs to be encrypted
    role_description = models.CharField(max_length=128, blank=True, help_text='A brief description of the user\'s role or permissions. (e.g., Guest, Admin)') # Needs to be encrypted
    notes = models.TextField(blank=True, help_text='Additional information about these credentials.') # Needs to be encrypted

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    environment = models.ForeignKey(Environment)

    class Meta:
        verbose_name_plural = 'Environment credentials'
        ordering = ['username', 'password']


class Engagement(models.Model):
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

    requestor = models.ForeignKey(Person, blank=True, null=True, help_text='Specify who requested this engagement.')
    application = models.ForeignKey(Application)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date']

    def save(self, *args, **kwargs):
        """Automatically sets the open and closed dates when the status changes."""
        if self.pk is not None:
            engagement = Engagement.objects.get(pk=self.pk)
            if engagement.status != self.status:
                if self.status == Engagement.PENDING_STATUS:
                    self.open_date = None
                    self.close_date = None
                elif self.status == Engagement.OPEN_STATUS:
                    self.open_date = timezone.now()
                    self.close_date = None
                elif self.status == Engagement.CLOSED_STATUS:
                    if self.open_date is None:
                        self.open_date = timezone.now()
                    self.close_date = timezone.now()

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


class ActivityType(models.Model):
    """Types of work."""

    name = models.CharField(max_length=128, unique=True, help_text='A unique name for this activity.')
    documentation = models.TextField(blank=True, help_text='Guidelines, procedures, and techniques for this activity type.')

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

    activity_type = models.ForeignKey(ActivityType)
    engagement = models.ForeignKey(Engagement)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.activity_type.name

    class Meta:
        ordering = ['engagement__start_date']
        verbose_name_plural = 'Activities'

    def save(self, *args, **kwargs):
        """Automatically sets the open and closed dates when the status changes."""
        if self.pk is not None:
            activity = Activity.objects.get(pk=self.pk)
            if activity.status != self.status:
                if self.status == Activity.PENDING_STATUS:
                    self.open_date = None
                    self.close_date = None
                elif self.status == Activity.OPEN_STATUS:
                    self.open_date = timezone.now()
                    self.close_date = None
                elif self.status == Activity.CLOSED_STATUS:
                    if self.open_date is None:
                        self.open_date = timezone.now()
                    self.close_date = timezone.now()

        super(Activity, self).save(*args, **kwargs)

    def is_pending(self):
        return self.status == Activity.PENDING_STATUS

    def is_open(self):
        return self.status == Activity.OPEN_STATUS

    def is_closed(self):
        return self.status == Activity.CLOSED_STATUS

    def is_ready_for_work(self):
        """If the activity is pending on or after the engagement's start date."""
        if self.status == Activity.PENDING_STATUS:
            if date.today() >= self.engagement.start_date:
                return True
        return False

    def is_past_due(self):
        """If the activity is not closed by the engagement's end date."""
        if self.status == Activity.PENDING_STATUS or self.status == Activity.OPEN_STATUS:
            if date.today() > self.engagement.end_date:
                return True
        return False


class Comment(models.Model):
    """Abstract message about an engagement or activity."""

    message = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.message

    class Meta:
        abstract = True


class EngagementComment(Comment): # Extends Comment
    """Comment for a specific engagement."""

    engagement = models.ForeignKey(Engagement)


class ActivityComment(Comment): # Extends Comment
    """Comment for a specific activity."""

    activity = models.ForeignKey(Activity)


class FileUpload(models.Model):
    """Abstract file upload by a user."""

    file = models.FileField()

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

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

    file_type = models.CharField(max_length=13, choices=FILE_TYPE_CHOICES)

    application = models.ForeignKey(Application)

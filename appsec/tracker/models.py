import datetime

from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Tag(models.Model):
    """Associated with application for search and catagorization."""

    color_regex = RegexValidator(regex=r'^[0-9A-Fa-f]{6}$', message="Color must be entered in the 6 characters hex format. (e.g., 'd94d59')")

    name = models.CharField(max_length=128, unique=True)
    color = models.CharField(max_length=6, validators=[color_regex])

    def __str__(self):
        return self.name

    # Overriding
    def save(self, *args, **kwargs):
        self.color = self.color.lower() # Convert to lowercase
        super(Tag, self).save(*args, **kwargs)


class Organization(models.Model):
    """Entities under which applications belong."""

    name = models.CharField(max_length=32, unique=True, help_text='A unique name for the organization.')
    description = models.TextField(blank=True, help_text='Information about the organization\'s purpose, history, and structure.')

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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class ThreadFix(models.Model):
    """ThreadFix server connection information."""

    name = models.CharField(max_length=32, unique=True, help_text='A unique name describing the ThreadFix server.')
    host = models.URLField(help_text='The URL for the ThreadFix server. (e.g., http://localhost:8080/threadfix/)')
    api_key = models.CharField(max_length=50, help_text='The API key can be generated on the ThreadFix API Key page.') # https://github.com/denimgroup/threadfix/blob/dev/threadfix-main/src/main/java/com/denimgroup/threadfix/service/APIKeyServiceImpl.java#L103

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ThreadFix"
        verbose_name_plural = 'ThreadFix'


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

    DEFINE_LIFECYCLE = 1
    DESIGN_LIFECYCLE = 2
    DEVELOP_LIFECYCLE = 3
    DEPLOY_LIFECYCLE = 4
    MAINTAIN_LIFECYCLE = 5
    LIFECYCLE_CHOICES = (
        (None, 'Not Specified'),
        (DEFINE_LIFECYCLE, 'Define'),
        (DESIGN_LIFECYCLE, 'Design'),
        (DEVELOP_LIFECYCLE, 'Develop'),
        (DEPLOY_LIFECYCLE, 'Deploy'),
        (MAINTAIN_LIFECYCLE, 'Maintain'),
    )

    THIRD_PARTY_LIBRARY_ORIGIN = 1
    PURCHASED_ORIGIN = 2
    CONTRACTOR_ORIGIN = 3
    INTERNALLY_DEVELOPED_ORIGIN = 4
    OPEN_SOURCE_ORIGIN = 5
    OUTSOURCED_ORIGIN = 6
    ORIGIN_CHOICES = (
        (None, 'Not Specified'),
        (THIRD_PARTY_LIBRARY_ORIGIN, 'Third Party Library'),
        (PURCHASED_ORIGIN, 'Purchased'),
        (CONTRACTOR_ORIGIN, 'Contractor'),
        (INTERNALLY_DEVELOPED_ORIGIN, 'Internally Developed'),
        (OPEN_SOURCE_ORIGIN, 'Open Source'),
        (OUTSOURCED_ORIGIN, 'Outsourced'),
    )

    AEROSPACE_INDUSTRY = 1
    AGRICULTURE_INDUSTRY = 2
    APPAREL_INDUSTRY = 3
    AUTOMOTIVE_TRANSPORT_INDUSTRY = 4
    BANKING_INDUSTRY = 5
    BEVERAGES_INDUSTRY = 6
    BIOTECHNOLOGY_INDUSTRY = 7
    BUSINESS_SERVICES_INDUSTRY = 8
    CHARITABLE_ORGANIZATIONS_INDUSTRY = 9
    CHEMICALS_INDUSTRY = 10
    COMMUNICATIONS_INDUSTRY = 11
    COMPUTER_HARDWARE_INDUSTRY = 12
    CONSULTING_INDUSTRY = 13
    CONSTRUCTION_INDUSTRY = 14
    CONSUMER_PRODUCTS_MANUFACTURERS_INDUSTRY = 15
    CONSUMER_SERVICES_INDUSTRY = 16
    CULTURAL_INSTITUTIONS_INDUSTRY = 17
    EDUCATION_INDUSTRY = 18
    ELECTRONICS_INDUSTRY = 19
    ENERGY_INDUSTRY = 20
    ENGINEERING_INDUSTRY = 21
    ENVIRONMENTAL_INDUSTRY = 22
    FINANCE_INDUSTRY = 23
    FOOD_BEVERAGE_INDUSTRY = 24
    FOUNDATIONS_INDUSTRY = 25
    GOVERNMENT_INDUSTRY = 26
    HEALTHCARE_INDUSTRY = 27
    HOSPITALITY_INDUSTRY = 28
    INSURANCE_INDUSTRY = 29
    MANUFACTURING_INDUSTRY = 30
    MACHINERY_INDUSTRY = 31
    MEDIA_ENTERTAINMENT_INDUSTRY = 32
    MEMBERSHIP_ORGANIZATIONS_INDUSTRY = 33
    METALS_MINING_INDUSTRY = 34
    OTHER_INDUSTRY = 35
    PHARMACEUTICALS_INDUSTRY = 36
    REAL_ESTATE_INDUSTRY = 37
    RECREATION_INDUSTRY = 38
    RETAIL_INDUSTRY = 39
    SECURITY_PRODUCTS_SERVICES_INDUSTRY = 40
    SOFTWARE_INDUSTRY = 41
    TECHNOLOGY_INDUSTRY = 42
    TELECOMMUNICATIONS_EQUIPMENT_INDUSTRY = 43
    TELECOMMUNICATIONS_INDUSTRY = 44
    TRANSPORTATION_INDUSTRY = 45
    UTILITIES_INDUSTRY = 46
    INDUSTRY_CHOICES = (
        (None, 'Not Specified'),
        (AEROSPACE_INDUSTRY, 'Aerospace'),
        (AGRICULTURE_INDUSTRY, 'Agriculture'),
        (APPAREL_INDUSTRY, 'Apparel'),
        (AUTOMOTIVE_TRANSPORT_INDUSTRY, 'Automotive and Transport'),
        (BANKING_INDUSTRY, 'Banking'),
        (BEVERAGES_INDUSTRY, 'Beverages'),
        (BIOTECHNOLOGY_INDUSTRY, 'Biotechnology'),
        (BUSINESS_SERVICES_INDUSTRY, 'Business Services'),
        (CHARITABLE_ORGANIZATIONS_INDUSTRY, 'Charitable Organizations'),
        (CHEMICALS_INDUSTRY, 'Chemicals'),
        (COMMUNICATIONS_INDUSTRY, 'Communications'),
        (COMPUTER_HARDWARE_INDUSTRY, 'Computer Hardware'),
        (CONSULTING_INDUSTRY, 'Consulting'),
        (CONSTRUCTION_INDUSTRY, 'Construction'),
        (CONSUMER_PRODUCTS_MANUFACTURERS_INDUSTRY, 'Consumer Products Manufacturers'),
        (CONSUMER_SERVICES_INDUSTRY, 'Consumer Services'),
        (CULTURAL_INSTITUTIONS_INDUSTRY, 'Cultural Institutions'),
        (EDUCATION_INDUSTRY, 'Education'),
        (ELECTRONICS_INDUSTRY, 'Electronics'),
        (ENERGY_INDUSTRY, 'Energy'),
        (ENGINEERING_INDUSTRY, 'Engineering'),
        (ENVIRONMENTAL_INDUSTRY, 'Environmental'),
        (FINANCE_INDUSTRY, 'Finance'),
        (FOOD_BEVERAGE_INDUSTRY, 'Food and Beverage'),
        (FOUNDATIONS_INDUSTRY, 'Foundations'),
        (GOVERNMENT_INDUSTRY, 'Government'),
        (HEALTHCARE_INDUSTRY, 'Healthcare'),
        (HOSPITALITY_INDUSTRY, 'Hospitality'),
        (INSURANCE_INDUSTRY, 'Insurance'),
        (MANUFACTURING_INDUSTRY, 'Manufacturing'),
        (MACHINERY_INDUSTRY, 'Machinery'),
        (MEDIA_ENTERTAINMENT_INDUSTRY, 'Media and Entertainment'),
        (MEMBERSHIP_ORGANIZATIONS_INDUSTRY, 'Membership Organizations'),
        (METALS_MINING_INDUSTRY, 'Metals and Mining'),
        (OTHER_INDUSTRY, 'Other'),
        (PHARMACEUTICALS_INDUSTRY, 'Pharmaceuticals'),
        (REAL_ESTATE_INDUSTRY, 'Real Estate'),
        (RECREATION_INDUSTRY, 'Recreation'),
        (RETAIL_INDUSTRY, 'Retail'),
        (SECURITY_PRODUCTS_SERVICES_INDUSTRY, 'Security Products and Services'),
        (SOFTWARE_INDUSTRY, 'Software'),
        (TECHNOLOGY_INDUSTRY, 'Technology'),
        (TELECOMMUNICATIONS_EQUIPMENT_INDUSTRY, 'Telecommunications Equipment'),
        (TELECOMMUNICATIONS_INDUSTRY, 'Telecommunications'),
        (TRANSPORTATION_INDUSTRY, 'Transportation'),
        (UTILITIES_INDUSTRY, 'Utilities'),
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


    # REGULATION_PCI = 1
    # REGULATION_HIPAA = 2
    # REGULATION_FERPA = 3
    # REGULATION_CHOICES = (
    #     (None, 'Not Specified'),
    #     (REGULATION_FERPA, 'FERPA'),
    #     (REGULATION_HIPAA, 'HIPAA'),
    #     (REGULATION_PCI, 'PCI')
    # )

    # General
    name = models.CharField(max_length=128, unique=True, help_text='A unique name for the application.')
    description = models.TextField(blank=True, help_text='Information about the application\'s purpose, history, and design.')

    # Metadata
    platform = models.CharField(max_length=11, choices=PLATFORM_CHOICES, blank=True, null=True)
    lifecycle = models.IntegerField(choices=LIFECYCLE_CHOICES, blank=True, null=True)
    origin = models.IntegerField(choices=ORIGIN_CHOICES, blank=True, null=True)
    industry = models.IntegerField(choices=INDUSTRY_CHOICES, blank=True, null=True)
    business_criticality = models.CharField(max_length=9, choices=BUSINESS_CRITICALITY_CHOICES, blank=True, null=True)
    approximate_users = models.PositiveIntegerField(blank=True, null=True, help_text='Estimate the number of user records within the application.')
    external_audience = models.BooleanField(default=False, help_text='Specify if the application is used by people outside the organization.')
    internet_accessible = models.BooleanField(default=False, help_text='Specify if the application is accessible from the public internet.')

    # Data Classification
    data_elements = models.ManyToManyField(DataElement, blank=True, null=True)
    override_dcl = models.IntegerField(choices=DATA_CLASSIFICATION_CHOICES, blank=True, null=True, help_text='Overrides the calculated data classification level.')
    override_reason = models.TextField(blank=True, help_text='Specify why the calculated data classification level is being overridden.')

    # ThreadFix
    threadfix = models.ForeignKey(ThreadFix, blank=True, null=True)
    threadfix_organization_id = models.PositiveIntegerField(blank=True, null=True)
    threadfix_application_id = models.PositiveIntegerField(blank=True, null=True)

    # Misc
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    #regulation = models.IntegerField(choices=REGULATION_CHOICES, blank=True, null=True)

    #source code repo
    #bug tracking tool
    #developer experience / familiarity
    #finance data
    #programming language/s
    #id for whitehat + checkmarx (third-party ids)
    #password policy

    organization = models.ForeignKey(Organization)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        get_latest_by = "modified_date"
        ordering = ['name']

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

    def __str__(self):
        return self.application.name + ' ' + dict(Environment.ENVIRONMENT_CHOICES)[self.environment_type]

    class Meta:
        ordering = ['-testing_approved', 'environment_type']


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
    email = models.EmailField()
    phone_work = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    phone_mobile = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    job_title = models.CharField(max_length=128, blank=True)
    role = models.CharField(max_length=17, choices=ROLE_CHOICES)

    application = models.ManyToManyField(Application, through='Relation')

    def __str__(self):
        return self.last_name + ', ' + self.first_name

    class Meta:
        ordering = ['last_name']
        verbose_name_plural = 'People'


class Relation(models.Model):
    """Associates a person with an application with a role."""

    owner = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    person = models.ForeignKey(Person)
    application = models.ForeignKey(Application)

    def __str__(self):
        return self.person.first_name + ' ' + self.person.last_name + ', ' + self.application.name


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
    open_date = models.DateTimeField(blank=True, null=True)
    close_date = models.DateTimeField(blank=True, null=True)

    requestor = models.ForeignKey(Person, blank=True, null=True)
    application = models.ForeignKey(Application)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date']

    def is_pending(self):
        return self.status == Engagement.PENDING_STATUS

    def is_open(self):
        return self.status == Engagement.OPEN_STATUS

    def is_closed(self):
        return self.status == Engagement.CLOSED_STATUS

    def is_ready_for_work(self):
        """If the engagement is pending on or after the start date."""
        if self.status == Engagement.PENDING_STATUS:
            if datetime.date.today() >= self.start_date:
                return True
        return False

    def is_past_due(self):
        """If the engagement is not closed by the end date."""
        if self.status == Engagement.PENDING_STATUS or self.status == Engagement.OPEN_STATUS:
            if datetime.date.today() > self.end_date:
                return True
        return False


class ActivityType(models.Model): # Incomplete
    """Types of work."""

    name = models.CharField(max_length=128, unique=True, help_text='A unique name for this activity.')
    documentation = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    """A unit of work performed for an application over a duration."""

    APPSCAN_ACTIVITY_TYPE = 'appscan'
    CHECKMARX_ONBOARDING_ACTIVITY_TYPE = 'checkmarx'
    MANUAL_ASSESSMENT_ACTIVITY_TYPE = 'manual assessment'
    REPORTING_ACTIVITY_TYPE = 'reporting'
    RETEST_PREVIOUS_ACTIVITY_TYPE = 'retest'
    THREAT_MODEL_ACTIVITY_TYPE = 'threat model'
    TRAINING_ACTIVITY_TYPE = 'training'
    VERACODE_ONBOARDING_ACTIVITY_TYPE = 'veracode'
    WHITEHAT_ONBOARDING_ACTIVITY_TYPE = 'whitehat'
    ACTIVITY_TYPE_CHOICES = (
        ('Assessments', (
                ('external', 'External Penetration Test'),
                (APPSCAN_ACTIVITY_TYPE, 'IBM AppScan Dynamic Scan'),
                (MANUAL_ASSESSMENT_ACTIVITY_TYPE, 'Manual Assessment'),
                ('peer review', 'Peer Review'),
                (REPORTING_ACTIVITY_TYPE, 'Reporting'),
                (RETEST_PREVIOUS_ACTIVITY_TYPE, 'Retest Known Issues'),
            )
        ),
        ('Third-Party Services', (
                (CHECKMARX_ONBOARDING_ACTIVITY_TYPE, 'Checkmarx Onboarding'),
                (VERACODE_ONBOARDING_ACTIVITY_TYPE, 'Veracode Onboarding'),
                (WHITEHAT_ONBOARDING_ACTIVITY_TYPE, 'WhiteHat Onboarding'),
            )
        ),
        ('Other', (
                ('consulting', 'Consulting'),
                (TRAINING_ACTIVITY_TYPE, 'Training'),
                (THREAT_MODEL_ACTIVITY_TYPE, 'Threat Model'),
            )
        ),
    )

    PENDING_STATUS = 'pending'
    OPEN_STATUS = 'open'
    CLOSED_STATUS = 'closed'
    STATUS_CHOICES = (
        (PENDING_STATUS, 'Pending'),
        (OPEN_STATUS, 'Open'),
        (CLOSED_STATUS, 'Closed')
    )

    activity_type = models.CharField(max_length=17, choices=ACTIVITY_TYPE_CHOICES)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default=PENDING_STATUS)
    description = models.TextField(blank=True)
    open_date = models.DateTimeField(blank=True, null=True)
    close_date = models.DateTimeField(blank=True, null=True)

    engagement = models.ForeignKey(Engagement)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return dict(Activity.ACTIVITY_TYPE_CHOICES)[self.activity_type]

    class Meta:
        ordering = ['engagement__start_date']
        verbose_name_plural = 'Activities'

    def is_pending(self):
        return self.status == Activity.PENDING_STATUS

    def is_open(self):
        return self.status == Activity.OPEN_STATUS

    def is_closed(self):
        return self.status == Activity.CLOSED_STATUS

    def is_ready_for_work(self):
        """If the activity is pending on or after the engagement's start date."""
        if self.status == Activity.PENDING_STATUS:
            if datetime.date.today() >= self.engagement.start_date:
                return True
        return False

    def is_past_due(self):
        """If the activity is not closed by the engagement's end date."""
        if self.status == Activity.PENDING_STATUS or self.status == Activity.OPEN_STATUS:
            if datetime.date.today() > self.engagement.end_date:
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

    REPORT_FILE_TYPE = 1
    DOCUMENTATION_FILE_TYPE = 2
    FILE_TYPE_CHOICES = (
        (REPORT_FILE_TYPE, 'Report'),
        (DOCUMENTATION_FILE_TYPE, 'Documentation'),
    )

    file_type = models.IntegerField(choices=FILE_TYPE_CHOICES)

    application = models.ForeignKey(Application)

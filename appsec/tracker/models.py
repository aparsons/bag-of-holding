from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.

class Tag(models.Model):
    """Associated with application for search and catagorization."""

    color_regex = RegexValidator(regex=r'^[0-9A-Fa-f]{6}$', message="Color must be entered in the hex format: 'd94d59'. Only 6 characters allowed.")

    name = models.CharField(max_length=128, unique=True)
    color = models.CharField(max_length=6, validators=[color_regex])

    def __str__(self):
        return self.name

    # Overriding
    def save(self, *args, **kwargs):
        self.color = self.color.lower() # Convert to lowercase
        super(Tag, self).save(*args, **kwargs)


class Application(models.Model):
    """Contains infomation about a software application."""

    WEB_PLATFORM = 1
    DESKTOP_PLATFORM = 2
    MOBILE_PLATFORM = 3
    PLATFORM_CHOICES = (
        (None, 'Not Specified'),
        (WEB_PLATFORM, 'Web'),
        (DESKTOP_PLATFORM, 'Desktop'),
        (MOBILE_PLATFORM, 'Mobile'),
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

    VERY_HIGH_CRITICALITY = 1
    HIGH_CRITICALITY = 2
    MEDIUM_CRITICALITY = 3
    LOW_CRITICALITY = 4
    VERY_LOW_CRITICALITY = 5
    NONE_CRITICALITY = 6
    BUSINESS_CRITICALITY_CHOICES = (
        (None, 'Not Specified'),
        (VERY_HIGH_CRITICALITY, 'Very High'),
        (HIGH_CRITICALITY, 'High'),
        (MEDIUM_CRITICALITY, 'Medium'),
        (LOW_CRITICALITY, 'Low'),
        (VERY_LOW_CRITICALITY, 'Very Low'),
        (NONE_CRITICALITY, 'None'),
    )

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    platform = models.IntegerField(choices=PLATFORM_CHOICES, blank=True, null=True)
    lifecycle = models.IntegerField(choices=LIFECYCLE_CHOICES, blank=True, null=True)
    origin = models.IntegerField(choices=ORIGIN_CHOICES, blank=True, null=True)
    industry = models.IntegerField(choices=INDUSTRY_CHOICES, blank=True, null=True)
    business_criticality = models.IntegerField(choices=BUSINESS_CRITICALITY_CHOICES, blank=True, null=True)
    external_audience = models.BooleanField(default=False)
    internet_accessible = models.BooleanField(default=False)
    #threadfix_application_id = models.IntegerField(unique=True)

    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name


class Environment(models.Model):
    """Container for information about a web server environment."""

    DEVELOPMENT_ENVIRONMENT = 'DEV'
    INTEGRATION_ENVIRONMENT = 'INT'
    QUALITY_ASSURANCE_ENVIRONMENT = 'QA'
    PRE_PRODUCTION_ENVIRONMENT = 'PPE'
    CUSTOMER_ACCEPTANCE_ENVIRONMENT = 'CAT'
    PRODUCTION_ENVIRONMENT = 'PROD'
    ENVIRONMENT_CHOICES = (
        (DEVELOPMENT_ENVIRONMENT, 'Development'),
        (INTEGRATION_ENVIRONMENT, 'Integration'),
        (QUALITY_ASSURANCE_ENVIRONMENT, 'Quality Assurance'),
        (PRE_PRODUCTION_ENVIRONMENT, 'Pre-Production'),
        (CUSTOMER_ACCEPTANCE_ENVIRONMENT, 'Customer Acceptance'),
        (PRODUCTION_ENVIRONMENT, 'Production'),
    )

    environment_type = models.CharField(max_length=4, choices=ENVIRONMENT_CHOICES)
    description = models.TextField(blank=True)
    testing_approved = models.BooleanField(default=False)

    application = models.ForeignKey(Application)

    def __str__(self):
        return self.application.name + ' ' + dict(Environment.ENVIRONMENT_CHOICES)[self.environment_type]


class EnvironmentLocation(models.Model):
    """URL for a specific environment"""

    location = models.URLField()
    notes = models.TextField(blank=True)

    environment = models.ForeignKey(Environment)

    def __str__(self):
        return self.location


class EnvironmentCredentials(models.Model):
    """Credentials for a specific environment."""

    username = models.CharField(max_length=255, blank=True) # Needs to be encrypted
    password = models.CharField(max_length=255, blank=True) # Needs to be encrypted
    notes = models.TextField(blank=True) # Needs to be encrypted

    environment = models.ForeignKey(Environment)

    class Meta:
        verbose_name_plural = 'Environment credentials'


class Person(models.Model):
    """Information about a person."""

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_work = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    phone_mobile = models.CharField(max_length=15, validators=[phone_regex], blank=True)

    application = models.ManyToManyField(Application, through='Relation')

    def __str__(self):
        return self.last_name + ', ' + self.first_name

    class Meta:
        ordering = ['last_name']
        verbose_name_plural = 'People'


class Relation(models.Model):
    """Associates a person with an application with a role."""

    DEVELOPER_ROLE = 1
    QUALITY_ASSURANCE_ROLE = 2
    OPERATIONS_ROLE = 3
    MANAGER_ROLE = 4
    SECURITY_OFFICER_ROLE = 5
    SECURITY_CHAMPION_ROLE = 6
    ROLE_CHOICES = (
        (DEVELOPER_ROLE, 'Developer'),
        (QUALITY_ASSURANCE_ROLE, 'Quality Assurance'),
        (OPERATIONS_ROLE, 'Operations'),
        (MANAGER_ROLE, 'Manager'),
        (SECURITY_OFFICER_ROLE, 'Security Officer'),
        (SECURITY_CHAMPION_ROLE, 'Security Champion'),
    )

    owner = models.BooleanField(default=False)
    role = models.IntegerField(choices=ROLE_CHOICES)
    notes = models.TextField(blank=True)

    person = models.ForeignKey(Person)
    application = models.ForeignKey(Application)

    def __str__(self):
        return self.person.first_name + ' ' + self.person.last_name + ', ' + self.application.name + ' ' + dict(Relation.ROLE_CHOICES)[self.role]


class Engagement(models.Model):
    """Container for activities performed for an application over a duration."""

    OPEN_STATUS = 1
    CLOSED_STATUS = 2
    STATUS_CHOICES = (
        (OPEN_STATUS, 'Open'),
        (CLOSED_STATUS, 'Closed'),
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=OPEN_STATUS)
    start_date = models.DateField()
    end_date = models.DateField()
    open_date = models.DateTimeField(blank=True, null=True)
    close_date = models.DateTimeField(blank=True, null=True)

    application = models.ForeignKey(Application)


class Activity(models.Model):
    """A unit of work performed for an application over a duration."""

    APPSCAN_ACTIVITY_TYPE = 1
    MANUAL_ASSESSMENT_ACTIVITY_TYPE = 2
    ACTIVITY_TYPE_CHOICES = (
        (APPSCAN_ACTIVITY_TYPE, 'IBM AppScan Dynamic Scan'),
        (MANUAL_ASSESSMENT_ACTIVITY_TYPE, 'Manual Assessment'),
    )

    OPEN_STATUS = 1
    CLOSED_STATUS = 2
    STATUS_CHOICES = (
        (OPEN_STATUS, 'Open'),
        (CLOSED_STATUS, 'Closed'),
    )

    activity_type = models.IntegerField(choices=ACTIVITY_TYPE_CHOICES)
    status = models.IntegerField(choices=STATUS_CHOICES, default=OPEN_STATUS)
    start_date = models.DateField()
    end_date = models.DateField()
    open_date = models.DateTimeField(blank=True, null=True)
    close_date = models.DateTimeField(blank=True, null=True)

    engagement = models.ForeignKey(Engagement)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    class Meta:
        verbose_name_plural = 'Activities'


class Note(models.Model):
    """Abstract message about an engagement or activity."""

    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.message

    class Meta:
        abstract = True


class EngagementNote(Note): # Extends Note
    """Note for a specific engagement."""

    engagement = models.ForeignKey(Engagement)


class ActivityNote(Note): # Extends Note
    """Note for a specific activity."""

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

    application = models.ForeignKey(Application)

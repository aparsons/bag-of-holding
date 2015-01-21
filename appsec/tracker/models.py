from django.db import models

# Create your models here.
class Application(models.Model):
    WEB_PLATFORM = 1
    DESKTOP_PLATFORM = 2
    MOBILE_PLATFORM = 3
    PLATFORM_CHOICES = (
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
    BUSINESS_CRITICALITY_CHOICES = (
        (VERY_HIGH_CRITICALITY, 'Very High'),
        (HIGH_CRITICALITY, 'High'),
        (MEDIUM_CRITICALITY, 'Medium'),
        (LOW_CRITICALITY, 'Low'),
        (VERY_LOW_CRITICALITY, 'Very Low'),
    )

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    platform = models.IntegerField(choices=PLATFORM_CHOICES)
    lifecycle = models.IntegerField(choices=LIFECYCLE_CHOICES)
    origin = models.IntegerField(choices=ORIGIN_CHOICES)
    industry = models.IntegerField(choices=INDUSTRY_CHOICES)
    business_criticality = models.IntegerField(choices=BUSINESS_CRITICALITY_CHOICES)
    external_audience = models.BooleanField(default=False)
    internet_accessible = models.BooleanField(default=False)
    #threadfix_application_id = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.name

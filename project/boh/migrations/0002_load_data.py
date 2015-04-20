# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def load_data(apps, schema_editor):
    """Loads the initial data into the application."""

    # Activity Types
    ActivityType = apps.get_model('boh', 'ActivityType')

    ActivityType.objects.create(name='External Penetration Test')
    ActivityType.objects.create(name='IBM AppScan Dynamic Scan')
    ActivityType.objects.create(name='Manual Assessment')
    ActivityType.objects.create(name='Peer Review')
    ActivityType.objects.create(name='Reporting')
    ActivityType.objects.create(name='Retest Known Issues')
    ActivityType.objects.create(name='Checkmarx Onboarding')
    ActivityType.objects.create(name='WhiteHat Onboarding')
    ActivityType.objects.create(name='Veracode Onboarding')
    ActivityType.objects.create(name='Consulting')
    ActivityType.objects.create(name='Training')
    ActivityType.objects.create(name='Threat Model')

    # Data Elements
    DataElement = apps.get_model('boh', 'DataElement')

    DataElement.objects.create(name='First Name', category='personal', weight=2)
    DataElement.objects.create(name='Last Name', category='global', weight=10)
    DataElement.objects.create(name='Email', category='global', weight=10)
    DataElement.objects.create(name='Phone Number', category='personal', weight=2)
    DataElement.objects.create(name='Fax Number', category='personal', weight=2)
    DataElement.objects.create(name='Address', category='personal', weight=2)
    DataElement.objects.create(name='Zip Code', category='personal', weight=5)
    DataElement.objects.create(name='Age', category='personal', weight=15)
    DataElement.objects.create(name='Gender', category='personal', weight=3)
    DataElement.objects.create(name='Marital Status', category='personal', weight=20)
    DataElement.objects.create(name='Family Information', category='personal', weight=20)
    DataElement.objects.create(name='Race', category='personal', weight=15)
    DataElement.objects.create(name='Religion', category='personal', weight=15)
    DataElement.objects.create(name='Date of Birth', category='personal', weight=15)
    DataElement.objects.create(name='Political Opinion', category='personal', weight=15)
    DataElement.objects.create(name='Disability Status', category='personal', weight=50)
    DataElement.objects.create(name='Education', category='personal', weight=100)
    DataElement.objects.create(name='Company Trade Secrets', category='company', weight=150)
    DataElement.objects.create(name='Company Source Code Repository', category='company', weight=100)
    DataElement.objects.create(name='Unannounced Financial Information', category='company', weight=150)
    DataElement.objects.create(name='Confidential Documentation', category='company', weight=100)
    DataElement.objects.create(name='Public Company Information', category='company', weight=1)
    DataElement.objects.create(name='Public Documentation', category='company', weight=1)
    DataElement.objects.create(name='Internal Support Documentation', category='company', weight=20)
    DataElement.objects.create(name='Public Cryptographic Keys', category='company', weight=1)
    DataElement.objects.create(name='Private Cryptographic Keys', category='company', weight=150)
    DataElement.objects.create(name='Numeric Identification Codes (PINs)', category='company', weight=150)
    DataElement.objects.create(name='Tokens (Hardware or Software)', category='company', weight=150)
    DataElement.objects.create(name='Single Sign On Credentials/Profiles', category='company', weight=150)
    DataElement.objects.create(name='Wallet', category='company', weight=150)
    DataElement.objects.create(name='Self Evaluation Test Scores', category='student', weight=1)
    DataElement.objects.create(name='Historical Examination Papers (Public)', category='student', weight=1)
    DataElement.objects.create(name='Sample Examination Papers (Public)', category='student', weight=1)
    DataElement.objects.create(name='Future Examination Papers (Non-Public)', category='student', weight=100)
    DataElement.objects.create(name='Historical Examination Papers (Non-Public)', category='student', weight=100)
    DataElement.objects.create(name='Confidential Transcripts (Non-Public)', category='student', weight=100)
    DataElement.objects.create(name='Confidential Test Scores (Non-Public)', category='student', weight=100)
    DataElement.objects.create(name='Financial Aid Records', category='student', weight=100)
    DataElement.objects.create(name='Last School Attended', category='student', weight=100)
    DataElement.objects.create(name='Degrees & Honors', category='student', weight=100)
    DataElement.objects.create(name='Social Security Number', category='government', weight=100)
    DataElement.objects.create(name='Tax Identifier', category='government', weight=100)
    DataElement.objects.create(name='Government Employee Number', category='government', weight=75)
    DataElement.objects.create(name='Drivers License Number', category='government', weight=100)
    DataElement.objects.create(name='Vehicle Registration', category='government', weight=75)
    DataElement.objects.create(name='Student Number', category='government', weight=75)
    DataElement.objects.create(name='Personal Account Number', category='pci', weight=150)
    DataElement.objects.create(name='Cardholder Name', category='pci', weight=150)
    DataElement.objects.create(name='Credit Card Number', category='pci', weight=150)
    DataElement.objects.create(name='CAV2/CVC2/CVV2/CID', category='pci', weight=150)
    DataElement.objects.create(name='Card Expiration Date', category='pci', weight=150)
    DataElement.objects.create(name='Credit History', category='pci', weight=150)
    DataElement.objects.create(name='Banking Account Numbers', category='pci', weight=150)
    DataElement.objects.create(name='Order Numbers', category='pci', weight=25)
    DataElement.objects.create(name='Invoice Details', category='pci', weight=25)
    DataElement.objects.create(name='Medical Record Details', category='medical', weight=150)
    DataElement.objects.create(name='Health Plan Beneficiary Details', category='medical', weight=150)


class Migration(migrations.Migration):

    dependencies = [
        ('boh', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]

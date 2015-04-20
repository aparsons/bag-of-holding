# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def load_regulations(apps, schema_editor):
    """Loads the initial data for regulations."""

    PRIVACY_CATEGORY = 'privacy'
    FINANCE_CATEGORY = 'finance'
    EDUCATION_CATEGORY = 'education'
    MEDICAL_CATEGORY = 'medical'

    UNITED_STATES_JURISDICTION = 'United States'
    CALIFORNIA_JURISDICTION = 'United States, California'
    EUROPEAN_UNION_JURISDICTION = 'European Union'
    UNITED_KINGDOM_JURISDICTION = 'United Kingdom'
    CANADA_JURISDICTION = 'Canada'

    Regulation = apps.get_model('boh', 'Regulation')

    Regulation.objects.create(
        name='Payment Card Industry Data Security Standard',
        acronym='PCI DSS',
        category=FINANCE_CATEGORY,
        jurisdiction=UNITED_STATES_JURISDICTION,
        description='The Payment Card Industry Data Security Standard (PCI DSS) is a proprietary information security standard for organizations that handle branded credit cards from the major card schemes including Visa, MasterCard, American Express, Discover, and JCB.',
        reference='http://en.wikipedia.org/wiki/Payment_Card_Industry_Data_Security_Standard'
    )

    Regulation.objects.create(
        name='Health Insurance Portability and Accountability Act',
        acronym='HIPAA',
        category=MEDICAL_CATEGORY,
        jurisdiction=UNITED_STATES_JURISDICTION,
        description='The Health Insurance Portability and Accountability Act of 1996 (HIPAA) was enacted by the United States Congress and signed by President Bill Clinton in 1996. It has been known as the Kennedy–Kassebaum Act or Kassebaum-Kennedy Act after two of its leading sponsors. Title I of HIPAA protects health insurance coverage for workers and their families when they change or lose their jobs. Title II of HIPAA, known as the Administrative Simplification (AS) provisions, requires the establishment of national standards for electronic health care transactions and national identifiers for providers, health insurance plans, and employers.',
        reference='http://en.wikipedia.org/wiki/Health_Insurance_Portability_and_Accountability_Act'
    )

    Regulation.objects.create(
        name='Family Educational Rights and Privacy Act',
        acronym='FERPA',
        category=EDUCATION_CATEGORY,
        jurisdiction=UNITED_STATES_JURISDICTION,
        description='The Family Educational Rights and Privacy Act of 1974 (FERPA) is a United States federal law that gives parents access to their child\'s education records, an opportunity to seek to have the records amended, and some control over the disclosure of information from the records. With several exceptions, schools must have a student\'s consent prior to the disclosure of education records after that student is 18 years old. The law applies only to educational agencies and institutions that receive funding under a program administered by the U.S. Department of Education. Other regulations under this act, effective starting January 3, 2012, allow for greater disclosures of personal and directory student identifying information and regulate student IDs and e-mail addresses.',
        reference='http://en.wikipedia.org/wiki/Family_Educational_Rights_and_Privacy_Act'
    )

    Regulation.objects.create(
        name='Sarbanes–Oxley Act',
        acronym='SOX',
        category=FINANCE_CATEGORY,
        jurisdiction=UNITED_STATES_JURISDICTION,
        description='The Sarbanes–Oxley Act of 2002 (SOX) is a United States federal law that set new or enhanced standards for all U.S. public company boards, management and public accounting firms. There are also a number of provisions of the Act that also apply to privately held companies, for example the willful destruction of evidence to impede a Federal investigation.',
        reference='http://en.wikipedia.org/wiki/Sarbanes%E2%80%93Oxley_Act'
    )

    Regulation.objects.create(
        name='Gramm–Leach–Bliley Act',
        acronym='GLBA',
        category=FINANCE_CATEGORY,
        jurisdiction=UNITED_STATES_JURISDICTION,
        description='The Gramm–Leach–Bliley Act (GLBA) is an act of the 106th United States Congress. It repealed part of the Glass–Steagall Act of 1933, removing barriers in the market among banking companies, securities companies and insurance companies that prohibited any one institution from acting as any combination of an investment bank, a commercial bank, and an insurance company. With the bipartisan passage of the Gramm–Leach–Bliley Act, commercial banks, investment banks, securities firms, and insurance companies were allowed to consolidate. Furthermore, it failed to give to the SEC or any other financial regulatory agency the authority to regulate large investment bank holding companies.',
        reference='http://en.wikipedia.org/wiki/Gramm%E2%80%93Leach%E2%80%93Bliley_Act'
    )

    Regulation.objects.create(
        name='Personal Information Protection and Electronic Documents Act',
        acronym='PIPEDA',
        category=PRIVACY_CATEGORY,
        jurisdiction=CANADA_JURISDICTION,
        description='The Personal Information Protection and Electronic Documents Act (PIPEDA) is a Canadian law relating to data privacy. It governs how private sector organizations collect, use and disclose personal information in the course of commercial business. In addition, the Act contains various provisions to facilitate the use of electronic documents. PIPEDA became law on 13 April 2000 to promote consumer trust in electronic commerce. The act was also intended to reassure the European Union that the Canadian privacy law was adequate to protect the personal information of European citizens.',
        reference='http://en.wikipedia.org/wiki/Personal_Information_Protection_and_Electronic_Documents_Act'
    )

    Regulation.objects.create(
        name='Data Protection Act 1998',
        acronym='DPA',
        category=PRIVACY_CATEGORY,
        jurisdiction=UNITED_KINGDOM_JURISDICTION,
        description='The Data Protection Act 1998 (DPA) is an Act of Parliament of the United Kingdom of Great Britain and Northern Ireland which defines UK law on the processing of data on identifiable living people. It is the main piece of legislation that governs the protection of personal data in the UK. Although the Act itself does not mention privacy, it was enacted to bring British law into line with the EU data protection directive of 1995 which required Member States to protect people\'s fundamental rights and freedoms and in particular their right to privacy with respect to the processing of personal data. In practice it provides a way for individuals to control information about themselves. Most of the Act does not apply to domestic use, for example keeping a personal address book. Anyone holding personal data for other purposes is legally obliged to comply with this Act, subject to some exemptions. The Act defines eight data protection principles. It also requires companies and individuals to keep personal information to themselves.',
        reference='http://en.wikipedia.org/wiki/Data_Protection_Act_1998'
    )

    Regulation.objects.create(
        name='Children\'s Online Privacy Protection Act',
        acronym='COPPA',
        category=PRIVACY_CATEGORY,
        jurisdiction=UNITED_STATES_JURISDICTION,
        description='The Children\'s Online Privacy Protection Act of 1998 (COPPA) is a United States federal law that applies to the online collection of personal information by persons or entities under U.S. jurisdiction from children under 13 years of age. It details what a website operator must include in a privacy policy, when and how to seek verifiable consent from a parent or guardian, and what responsibilities an operator has to protect children\'s privacy and safety online including restrictions on the marketing to those under 13. While children under 13 can legally give out personal information with their parents\' permission, many websites disallow underage children from using their services altogether due to the amount of cash and work involved in the law compliance.',
        reference='http://en.wikipedia.org/wiki/Children%27s_Online_Privacy_Protection_Act'
    )

    Regulation.objects.create(
        name='California Security Breach Information Act',
        acronym='CA SB-1386',
        category=PRIVACY_CATEGORY,
        jurisdiction=CALIFORNIA_JURISDICTION,
        description='In the United States, the California Security Breach Information Act (SB-1386) is a California state law requiring organizations that maintain personal information about individuals to inform those individuals if the security of their information is compromised. The Act stipulates that if there\'s a security breach of a database containing personal data, the responsible organization must notify each individual for whom it maintained information. The Act, which went into effect July 1, 2003, was created to help stem the increasing incidence of identity theft.',
        reference='http://en.wikipedia.org/wiki/California_S.B._1386'
    )

    Regulation.objects.create(
        name='California Online Privacy Protection Act',
        acronym='OPPA',
        category=PRIVACY_CATEGORY,
        jurisdiction=CALIFORNIA_JURISDICTION,
        description='The California Online Privacy Protection Act of 2003 (OPPA), effective as of July 1, 2004, is a California State Law. According to this law, operators of commercial websites that collect Personally identifiable information from California\'s residents are required to conspicuously post and comply with a privacy policy that meets certain requirements.',
        reference='http://en.wikipedia.org/wiki/Online_Privacy_Protection_Act'
    )

    Regulation.objects.create(
        name='Data Protection Directive',
        acronym='Directive 95/46/EC',
        category=PRIVACY_CATEGORY,
        jurisdiction=EUROPEAN_UNION_JURISDICTION,
        description='The Data Protection Directive (officially Directive 95/46/EC on the protection of individuals with regard to the processing of personal data and on the free movement of such data) is a European Union directive adopted in 1995 which regulates the processing of personal data within the European Union. It is an important component of EU privacy and human rights law.',
        reference='http://en.wikipedia.org/wiki/Data_Protection_Directive'
    )

    Regulation.objects.create(
        name='Directive on Privacy and Electronic Communications',
        acronym='Directive 2002/58/EC',
        category=PRIVACY_CATEGORY,
        jurisdiction=EUROPEAN_UNION_JURISDICTION,
        description='Directive 2002/58 on Privacy and Electronic Communications, otherwise known as E-Privacy Directive, is an EU directive on data protection and privacy in the digital age. It presents a continuation of earlier efforts, most directly the Data Protection Directive. It deals with the regulation of a number of important issues such as confidentiality of information, treatment of traffic data, spam and cookies. This Directive has been amended by Directive 2009/136, which introduces several changes, especially in what concerns cookies, that are now subject to prior consent.',
        reference='http://en.wikipedia.org/wiki/Directive_on_Privacy_and_Electronic_Communications'
    )


def load_technologies(apps, schema_editor):
    """Loads the initial data for technologies."""

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

    Technology = apps.get_model('boh', 'Technology')

    # Programming Languages (24)
    Technology.objects.create(name='ActionScript', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='http://www.adobe.com/devnet/actionscript.html')
    Technology.objects.create(name='Assembly', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='http://en.wikipedia.org/wiki/Assembly_language')
    Technology.objects.create(name='C', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='http://en.wikipedia.org/wiki/C_(programming_language)')
    Technology.objects.create(name='C#', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='http://en.wikipedia.org/wiki/C_Sharp_(programming_language)')
    Technology.objects.create(name='C++', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='http://en.wikipedia.org/wiki/C%2B%2B')
    Technology.objects.create(name='COBOL', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='http://en.wikipedia.org/wiki/COBOL')
    Technology.objects.create(name='D', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='http://dlang.org/')
    Technology.objects.create(name='Delphi/Object Pascal', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='http://en.wikipedia.org/wiki/Object_Pascal')
    Technology.objects.create(name='F#', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='http://fsharp.org/')
    Technology.objects.create(name='Fortran', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='http://en.wikipedia.org/wiki/Fortran')
    Technology.objects.create(name='Go', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='https://golang.org/')
    Technology.objects.create(name='Groovy', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='http://www.groovy-lang.org/')
    Technology.objects.create(name='Java', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='https://www.java.com')
    Technology.objects.create(name='JavaScript', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='http://en.wikipedia.org/wiki/JavaScript')
    Technology.objects.create(name='Lua', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='http://www.lua.org/')
    Technology.objects.create(name='Objective-C', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/Introduction/Introduction.html')
    Technology.objects.create(name='Perl', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='https://www.perl.org/')
    Technology.objects.create(name='PHP', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='http://php.net/')
    Technology.objects.create(name='Python', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='https://www.python.org/')
    Technology.objects.create(name='Ruby', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='https://www.ruby-lang.org/')
    Technology.objects.create(name='Rust', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='http://www.rust-lang.org/')
    Technology.objects.create(name='Scala', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='http://www.scala-lang.org/')
    Technology.objects.create(name='Visual Basic', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='https://msdn.microsoft.com/en-us/vstudio/ms788229.aspx')
    Technology.objects.create(name='Visual Basic .NET', category=PROGRAMMING_LANGUAGE_CATEGORY, reference='https://msdn.microsoft.com/en-us/vstudio/hh388573')

    # Operating Systems (5)
    Technology.objects.create(name='Windows', category=OPERATING_SYSTEM_CATEGORY, reference='http://windows.microsoft.com/')
    Technology.objects.create(name='Linux', category=OPERATING_SYSTEM_CATEGORY, reference='http://en.wikipedia.org/wiki/Linux')
    Technology.objects.create(name='Macintosh OS X', category=OPERATING_SYSTEM_CATEGORY, reference='https://www.apple.com/osx/')
    Technology.objects.create(name='iOS', category=OPERATING_SYSTEM_CATEGORY, reference='https://www.apple.com/ios/')
    Technology.objects.create(name='Android', category=OPERATING_SYSTEM_CATEGORY, reference='https://www.android.com/')

    # Data Stores (13)
    Technology.objects.create(name='Cassandra', category=DATA_STORE_CATEGORY, reference='http://cassandra.apache.org/')
    Technology.objects.create(name='CouchDB', category=DATA_STORE_CATEGORY, reference='http://couchdb.apache.org/')
    Technology.objects.create(name='IBM DB2', category=DATA_STORE_CATEGORY, reference='http://www.ibm.com/software/data/db2/')
    Technology.objects.create(name='Memcached', category=DATA_STORE_CATEGORY, reference='http://memcached.org/')
    Technology.objects.create(name='Microsoft Access', category=DATA_STORE_CATEGORY, reference='https://products.office.com/en-us/access')
    Technology.objects.create(name='Microsoft SQL Server', category=DATA_STORE_CATEGORY, reference='http://www.microsoft.com/en-us/server-cloud/products/sql-server/')
    Technology.objects.create(name='MongoDB', category=DATA_STORE_CATEGORY, reference='https://www.mongodb.org/')
    Technology.objects.create(name='MySQL', category=DATA_STORE_CATEGORY, reference='https://www.mysql.com/')
    Technology.objects.create(name='Oracle', category=DATA_STORE_CATEGORY, reference='https://www.oracle.com/database/index.html')
    Technology.objects.create(name='PostgreSQL', category=DATA_STORE_CATEGORY, reference='http://www.postgresql.org/')
    Technology.objects.create(name='Redis', category=DATA_STORE_CATEGORY, reference='http://redis.io/')
    Technology.objects.create(name='SQLite', category=DATA_STORE_CATEGORY, reference='http://www.sqlite.org/')
    Technology.objects.create(name='Sybase', category=DATA_STORE_CATEGORY, reference='http://go.sap.com/index.html')

    # Frameworks (32)
    Technology.objects.create(name='Adobe AIR', category=FRAMEWORK_CATEGORY, reference='http://www.adobe.com/products/air.html')
    Technology.objects.create(name='AngularJS', category=FRAMEWORK_CATEGORY, reference='https://angularjs.org/')
    Technology.objects.create(name='ASP.NET', category=FRAMEWORK_CATEGORY, reference='http://www.asp.net/')
    Technology.objects.create(name='Backbone.js', category=FRAMEWORK_CATEGORY, reference='http://backbonejs.org/')
    Technology.objects.create(name='Bootstrap', category=FRAMEWORK_CATEGORY, reference='http://getbootstrap.com/')
    Technology.objects.create(name='CakePHP', category=FRAMEWORK_CATEGORY, reference='http://cakephp.org/')
    Technology.objects.create(name='CodeIgniter', category=FRAMEWORK_CATEGORY, reference='http://www.codeigniter.com/')
    Technology.objects.create(name='Django', category=FRAMEWORK_CATEGORY, reference='https://www.djangoproject.com/')
    Technology.objects.create(name='Express', category=FRAMEWORK_CATEGORY, reference='http://expressjs.com/')
    Technology.objects.create(name='Flask', category=FRAMEWORK_CATEGORY, reference='http://flask.pocoo.org/')
    Technology.objects.create(name='Flex', category=FRAMEWORK_CATEGORY, reference='http://www.adobe.com/products/flex.html')
    Technology.objects.create(name='Foundation', category=FRAMEWORK_CATEGORY, reference='http://foundation.zurb.com/')
    Technology.objects.create(name='Google Web Toolkit', category=FRAMEWORK_CATEGORY, reference='http://www.gwtproject.org/')
    Technology.objects.create(name='Grails', category=FRAMEWORK_CATEGORY, reference='http://www.grails.org/')
    Technology.objects.create(name='Ionic', category=FRAMEWORK_CATEGORY, reference='http://ionicframework.com/')
    Technology.objects.create(name='JavaServer Faces', category=FRAMEWORK_CATEGORY, reference='https://javaserverfaces.java.net/')
    Technology.objects.create(name='Laravel', category=FRAMEWORK_CATEGORY, reference='http://laravel.com/')
    Technology.objects.create(name='Meteor', category=FRAMEWORK_CATEGORY, reference='https://www.meteor.com/')
    Technology.objects.create(name='Mono', category=FRAMEWORK_CATEGORY, reference='http://www.mono-project.com/')
    Technology.objects.create(name='Nette', category=FRAMEWORK_CATEGORY, reference='http://nette.org/')
    Technology.objects.create(name='PhoneGap', category=FRAMEWORK_CATEGORY, reference='http://phonegap.com/')
    Technology.objects.create(name='PHPixie', category=FRAMEWORK_CATEGORY, reference='http://phpixie.com/')
    Technology.objects.create(name='Play', category=FRAMEWORK_CATEGORY, reference='https://www.playframework.com/')
    Technology.objects.create(name='Qt', category=FRAMEWORK_CATEGORY, reference='http://www.qt.io/')
    Technology.objects.create(name='Ruby on Rails', category=FRAMEWORK_CATEGORY, reference='http://rubyonrails.org/')
    Technology.objects.create(name='Spring', category=FRAMEWORK_CATEGORY, reference='http://spring.io/')
    Technology.objects.create(name='Struts', category=FRAMEWORK_CATEGORY, reference='http://struts.apache.org/')
    Technology.objects.create(name='Symfony', category=FRAMEWORK_CATEGORY, reference='http://symfony.com/')
    Technology.objects.create(name='Unity', category=FRAMEWORK_CATEGORY, reference='http://unity3d.com/')
    Technology.objects.create(name='Vaadin', category=FRAMEWORK_CATEGORY, reference='https://vaadin.com/')
    Technology.objects.create(name='Yii', category=FRAMEWORK_CATEGORY, reference='http://www.yiiframework.com/')
    Technology.objects.create(name='Zend', category=FRAMEWORK_CATEGORY, reference='http://framework.zend.com/')

    # Third Party Components (5)
    Technology.objects.create(name='Drupal', category=THIRD_PARTY_COMPONENT, reference='https://www.drupal.org/')
    Technology.objects.create(name='MediaWiki', category=THIRD_PARTY_COMPONENT, reference='https://www.mediawiki.org/')
    Technology.objects.create(name='phpBB', category=THIRD_PARTY_COMPONENT, reference='https://www.phpbb.com/')
    Technology.objects.create(name='vBulletin', category=THIRD_PARTY_COMPONENT, reference='https://www.vbulletin.com/')
    Technology.objects.create(name='Wordpress', category=THIRD_PARTY_COMPONENT, reference='https://wordpress.org/')

    # Web Servers (3)
    Technology.objects.create(name='Apache HTTPD', category=WEB_SERVER_CATEGORY, reference='http://httpd.apache.org/')
    Technology.objects.create(name='Microsoft IIS', category=WEB_SERVER_CATEGORY, reference='http://www.iis.net/')
    Technology.objects.create(name='nginx', category=WEB_SERVER_CATEGORY, reference='http://nginx.org/')

    # Application Servers (7)
    Technology.objects.create(name='Tomcat', category=APPLICATION_SERVER_CATEGORY, reference='http://tomcat.apache.org/')
    Technology.objects.create(name='ColdFusion', category=APPLICATION_SERVER_CATEGORY, reference='http://www.adobe.com/products/coldfusion-family.html')
    Technology.objects.create(name='WebSphere', category=APPLICATION_SERVER_CATEGORY, reference='http://www.ibm.com/software/websphere')
    Technology.objects.create(name='JBoss', category=APPLICATION_SERVER_CATEGORY, reference='http://www.jboss.org/')
    Technology.objects.create(name='WebLogic', category=APPLICATION_SERVER_CATEGORY, reference='http://www.oracle.com/technetwork/middleware/weblogic/overview/index-085209.html')
    Technology.objects.create(name='Node.js', category=APPLICATION_SERVER_CATEGORY, reference='https://nodejs.org/')
    Technology.objects.create(name='Gunicorn', category=APPLICATION_SERVER_CATEGORY, reference='http://gunicorn.org/')

    # Hosting Providers (5)
    Technology.objects.create(name='Amazon Web Services (AWS)', category=HOSTING_PROVIDER_CATEGORY, reference='http://aws.amazon.com/')
    Technology.objects.create(name='Google App Engine', category=HOSTING_PROVIDER_CATEGORY, reference='https://cloud.google.com/appengine/docs')
    Technology.objects.create(name='Heroku', category=HOSTING_PROVIDER_CATEGORY, reference='https://www.heroku.com/')
    Technology.objects.create(name='Microsoft Azure', category=HOSTING_PROVIDER_CATEGORY, reference='http://azure.microsoft.com/')
    Technology.objects.create(name='Rackspace', category=HOSTING_PROVIDER_CATEGORY, reference='http://www.rackspace.com/')

    # Denial of Service (4)
    Technology.objects.create(name='CloudFlare', category=DENIAL_OF_SERVICE_CATEGORY, reference='https://www.cloudflare.com/')
    Technology.objects.create(name='Akamai', category=DENIAL_OF_SERVICE_CATEGORY, reference='http://www.akamai.com/html/solutions/cloud-security-solutions.html')
    Technology.objects.create(name='Prolexic', category=DENIAL_OF_SERVICE_CATEGORY, reference='http://www.prolexic.com/')
    Technology.objects.create(name='Imperva Incapsula', category=DENIAL_OF_SERVICE_CATEGORY, reference='http://www.imperva.com/Products/DDosProtection')

    # Firewalls (5)
    Technology.objects.create(name='Barracuda WAF', category=FIREWALL_CATEGORY, reference='https://www.barracuda.com/products/webapplicationfirewall')
    Technology.objects.create(name='BIG-IP ASM', category=FIREWALL_CATEGORY, reference='https://f5.com/products/modules/application-security-manager')
    Technology.objects.create(name='Imperva SecureSphere', category=FIREWALL_CATEGORY, reference='http://www.imperva.com/Products/WebApplicationFirewall')
    Technology.objects.create(name='ModSecurity', category=FIREWALL_CATEGORY, reference='https://www.modsecurity.org/')
    Technology.objects.create(name='Qualys WAF', category=FIREWALL_CATEGORY, reference='https://www.qualys.com/enterprises/qualysguard/web-application-firewall/')


class Migration(migrations.Migration):

    dependencies = [
        ('boh', '0003_v1_0_1'),
    ]

    operations = [
        migrations.CreateModel(
            name='Regulation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the legislation.', max_length=128)),
                ('acronym', models.CharField(unique=True, help_text='A shortened representation of the name.', max_length=20)),
                ('category', models.CharField(help_text='The subject of the regulation.', choices=[('privacy', 'Privacy'), ('finance', 'Finance'), ('education', 'Education'), ('medical', 'Medical'), ('other', 'Other')], max_length=9)),
                ('jurisdiction', models.CharField(help_text='The territory over which the regulation applies.', max_length=64)),
                ('description', models.TextField(help_text="Information about the regulation's purpose.", blank=True)),
                ('reference', models.URLField(blank=True, help_text='An external URL for more information.')),
            ],
            options={
                'ordering': ['jurisdiction', 'category', 'name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ServiceLevelAgreement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the service level agreement.', max_length=64)),
                ('description', models.CharField(max_length=256, blank=True, help_text="Information about this service level agreement's scope, quality, and responsibilities.")),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the technology.', max_length=64)),
                ('category', models.CharField(help_text='The type of technology.', choices=[('language', 'Language'), ('operating system', 'Operating System'), ('data store', 'Data Store'), ('framework', 'Framework'), ('third-party component', 'Third-Party Component'), ('application server', 'Application Server'), ('web server', 'Web Server'), ('hosting provider', 'Hosting Provider'), ('denial of service', 'DDoS Protection'), ('firewall', 'Firewall')], max_length=21)),
                ('description', models.CharField(max_length=256, blank=True, help_text='Information about the technology.')),
                ('reference', models.URLField(blank=True, help_text='An external URL for more information.')),
            ],
            options={
                'ordering': ['category', 'name'],
                'verbose_name_plural': 'Technologies',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='application',
            name='regulations',
            field=models.ManyToManyField(null=True, blank=True, to='boh.Regulation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='service_level_agreements',
            field=models.ManyToManyField(null=True, blank=True, to='boh.ServiceLevelAgreement'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='technologies',
            field=models.ManyToManyField(null=True, blank=True, to='boh.Technology'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='application',
            name='business_criticality',
            field=models.CharField(null=True, max_length=9, choices=[('very high', 'Very High'), ('high', 'High'), ('medium', 'Medium'), ('low', 'Low'), ('very low', 'Very Low'), ('none', 'None')], blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='application',
            name='lifecycle',
            field=models.CharField(null=True, max_length=8, choices=[('idea', 'Idea'), ('explore', 'Explore'), ('validate', 'Validate'), ('grow', 'Grow'), ('sustain', 'Sustain'), ('retire', 'Retire')], blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='application',
            name='origin',
            field=models.CharField(null=True, max_length=19, choices=[('third party library', 'Third Party Library'), ('purchased', 'Purchased'), ('contractor', 'Contractor Developed'), ('internal', 'Internally Developed'), ('open source', 'Open Source'), ('outsourced', 'Outsourced')], blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='application',
            name='platform',
            field=models.CharField(null=True, max_length=11, choices=[('web', 'Web'), ('desktop', 'Desktop'), ('mobile', 'Mobile'), ('web service', 'Web Service')], blank=True),
            preserve_default=True,
        ),
        migrations.RunPython(load_regulations),
        migrations.RunPython(load_technologies),
    ]

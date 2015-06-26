import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from . import models


class TagTests(TestCase):

    def test_str(self):
        self.assertEqual('Name', models.Tag(name='Name', color='FFFFFF').__str__())

    def test_save(self):
        """Validates colors are always saved as lowercase."""
        tag = models.Tag(name='Test', color='FFFFFF')
        tag.save()
        self.assertEqual('ffffff', tag.color)


class PersonTests(TestCase):

    def setUp(self):
        self.person_1 = models.Person(first_name='f', last_name='l', email='f@l.com', role=models.Person.MANAGER_ROLE)
        self.person_1.phone_work = '3057806095'
        self.person_1.phone_mobile = '847-765-1008'

    def test_str(self):
        self.assertEqual('f l', self.person_1.__str__())

    def test_save(self):
        """Validates phone numbers will be saved in E164 format."""
        self.person_1.save()
        self.assertEqual('+13057806095', self.person_1.phone_work)
        self.assertEqual('+18477651008', self.person_1.phone_mobile)


class OrganizationTests(TestCase):

    def test_str(self):
        self.assertEqual('Name', models.Organization(name='Name').__str__())


class DataElementTests(TestCase):

    def test_str(self):
        element = models.DataElement(name='Test', description='', category=models.DataElement.GLOBAL_CATEGORY, weight=5)
        self.assertEqual('Test', element.__str__())


class TechnologyTests(TestCase):

    def setUp(self):
        self.tech_1 = models.Technology(name='Python', category=models.Technology.PROGRAMMING_LANGUAGE_CATEGORY,
                                        description='Only a test', reference='https://www.python.org/')

    def test_str(self):
        self.assertEqual('Language :: Python', self.tech_1.__str__())


class RegulationTests(TestCase):

    def setUp(self):
        self.reg_1 = models.Regulation(name='PCI Data Security Standard', acronym='PCI DSS',
                                       category=models.Regulation.FINANCE_CATEGORY, jurisdiction='United States',
                                       description='Test', reference='https://www.pcisecuritystandards.org/')

    def test_str(self):
        self.assertEqual('PCI DSS (United States)', self.reg_1.__str__())


class ServiceLevelAgreementTests(TestCase):

    def setUp(self):
        self.sla_1 = models.ServiceLevelAgreement(name='Test', description='Something')

    def test_str(self):
        self.assertEqual('Test', self.sla_1.__str__())


class ThreadFixTests(TestCase):

    def setUp(self):
        self.tf_1 = models.ThreadFix(name='TF', host='http://localhost:8080/', api_key='key', verify_ssl=True)

    def test_str(self):
        self.assertEqual('TF - http://localhost:8080/', self.tf_1.__str__())


class ApplicationTests(TestCase):

    def setUp(self):
        self.org_1 = models.Organization(name='Org1')
        self.org_1.save()

        self.de_fname = models.DataElement(name='fname', category=models.DataElement.PERSONAL_CATEGORY, weight=2.0)
        self.de_fname.save()

        self.de_lname = models.DataElement(name='lname', category=models.DataElement.GLOBAL_CATEGORY, weight=10.0)
        self.de_lname.save()

        self.de_gender = models.DataElement(name='gender', category=models.DataElement.PERSONAL_CATEGORY, weight=3.0)
        self.de_gender.save()

        self.de_age = models.DataElement(name='age', category=models.DataElement.PERSONAL_CATEGORY, weight=15.0)
        self.de_age.save()

        self.de_edu = models.DataElement(name='education', category=models.DataElement.PERSONAL_CATEGORY, weight=100.0)
        self.de_edu.save()

        self.app_1 = models.Application(name='App1', organization=self.org_1)
        self.app_1.save()
        self.app_1.data_elements.add(self.de_fname)
        self.app_1.data_elements.add(self.de_gender)
        self.app_1.save()

        self.app_2 = models.Application(name='App2', organization=self.org_1)
        self.app_2.save()
        self.app_2.data_elements.add(self.de_fname)
        self.app_2.data_elements.add(self.de_lname)
        self.app_2.data_elements.add(self.de_gender)
        self.app_2.created_date = timezone.utc.localize(datetime.datetime(2012, 3, 3, 1, 30))
        self.app_2.save()

        self.app_3 = models.Application(name='App3', organization=self.org_1)
        self.app_3.save()
        self.app_3.data_elements.add(self.de_age)
        self.app_3.data_elements.add(self.de_edu)
        self.app_3.save()

        self.app_4 = models.Application(name='App4', organization=self.org_1)
        self.app_4.save()
        self.app_4.data_elements.add(self.de_fname)
        self.app_4.data_elements.add(self.de_lname)
        self.app_4.data_elements.add(self.de_edu)
        self.app_4.save()

    def test_str(self):
        self.assertEqual('App1', self.app_1.__str__())

    def test_data_classification_level_1(self):
        # First Name, Gender
        self.assertEqual(5.0, self.app_1.data_sensitivity_value())
        self.assertEqual(models.Application.DCL_1, self.app_1.data_classification_level())

    def test_data_classification_level_2(self):
        # First Name, Last Name, Gender
        self.assertEqual(55.0, self.app_2.data_sensitivity_value())
        self.assertEqual(models.Application.DCL_2, self.app_2.data_classification_level())

    def test_data_classification_level_3(self):
        # Age, Education
        self.assertEqual(115.0, self.app_3.data_sensitivity_value())
        self.assertEqual(models.Application.DCL_3, self.app_3.data_classification_level())

    def test_data_classification_level_4(self):
        # First Name, Last Name, Education
        self.assertEqual(1122.0, self.app_4.data_sensitivity_value())
        self.assertEqual(models.Application.DCL_4, self.app_4.data_classification_level())

    def test_is_new(self):
        self.assertEqual(True, self.app_1.is_new())
        self.assertEqual(False, self.app_2.is_new())


class ThreadFixMetricsTests(TestCase):

    def setUp(self):
        self.tfm_1 = models.ThreadFixMetrics(critical_count=1, high_count=4, medium_count=16, low_count=10,
                                             informational_count=3)

    def test_total(self):
        self.assertEqual(34, self.tfm_1.total())


class RelationTests(TestCase):

    def setUp(self):
        self.org_1 = models.Organization(name='Org1')
        self.org_1.save()

        self.app_1 = models.Application(name='App1', organization=self.org_1)
        self.app_1.save()

        self.per_1 = models.Person(first_name='John', last_name='Doe', email='j@d.com', role=models.Person.MANAGER_ROLE)
        self.per_1.save()

        self.rel_1 = models.Relation(person=self.per_1, application=self.app_1)
        self.rel_1.save()

    def test_str(self):
        self.assertEqual('John Doe - App1', self.rel_1.__str__())


class EnvironmentTests(TestCase):

    def setUp(self):
        self.org_1 = models.Organization(name='Org1')
        self.org_1.save()

        self.app_1 = models.Application(name='App1', organization=self.org_1)
        self.app_1.save()

        self.env_1 = models.Environment(environment_type=models.Environment.PRODUCTION_ENVIRONMENT,
                                        application=self.app_1)
        self.env_1.save()

    def test_str(self):
        self.assertEqual('App1 (Production)', self.env_1.__str__())


class EnvironmentLocationTests(TestCase):

    def setUp(self):
        self.org_1 = models.Organization(name='Org1')
        self.org_1.save()

        self.app_1 = models.Application(name='App1', organization=self.org_1)
        self.app_1.save()

        self.env_1 = models.Environment(environment_type=models.Environment.PRODUCTION_ENVIRONMENT,
                                        application=self.app_1)
        self.env_1.save()

        self.el_1 = models.EnvironmentLocation(location='http://www.google.com/', environment=self.env_1)
        self.el_1.save()

    def test_str(self):
        self.assertEqual('http://www.google.com/', self.el_1.__str__())


class EnvironmentCredentialsTests(TestCase):

    def setUp(self):
        self.org_1 = models.Organization(name='Org1')
        self.org_1.save()

        self.app_1 = models.Application(name='App1', organization=self.org_1)
        self.app_1.save()

        self.env_1 = models.Environment(environment_type=models.Environment.PRODUCTION_ENVIRONMENT,
                                        application=self.app_1)
        self.env_1.save()

        self.ec_1 = models.EnvironmentCredentials(username='user', password='pass123', environment=self.env_1)
        self.ec_1.save()


class EngagementTests(TestCase):

    def setUp(self):
        self.org_1 = models.Organization(name='Org1')
        self.org_1.save()

        self.app_1 = models.Application(name='App1', organization=self.org_1)
        self.app_1.save()

        self.eng_1 = models.Engagement(start_date=datetime.date.today(),
                                       end_date=datetime.date.today() + datetime.timedelta(days=5),
                                       application=self.app_1)
        self.eng_1.save()

    def test_save_pending_to_open(self):
        self.eng_1.status = models.Engagement.PENDING_STATUS
        self.eng_1.save()

        self.eng_1.status = models.Engagement.OPEN_STATUS
        self.eng_1.save()

        self.assertNotEqual(None, self.eng_1.open_date)
        self.assertEqual(None, self.eng_1.close_date)

    def test_save_pending_to_closed(self):
        self.eng_1.status = models.Engagement.PENDING_STATUS
        self.eng_1.save()

        self.eng_1.status = models.Engagement.CLOSED_STATUS
        self.eng_1.save()

        self.assertNotEqual(None, self.eng_1.open_date)
        self.assertNotEqual(None, self.eng_1.close_date)
        self.assertEqual(self.eng_1.open_date, self.eng_1.close_date)

    def test_save_open_to_pending(self):
        self.eng_1.status = models.Engagement.OPEN_STATUS
        self.eng_1.save()

        self.eng_1.status = models.Engagement.PENDING_STATUS
        self.eng_1.save()

        self.assertEqual(None, self.eng_1.open_date)
        self.assertEqual(None, self.eng_1.close_date)

    def test_save_open_to_closed(self):
        self.eng_1.status = models.Engagement.OPEN_STATUS
        self.eng_1.save()

        self.eng_1.status = models.Engagement.CLOSED_STATUS
        self.eng_1.save()

        self.assertNotEqual(None, self.eng_1.open_date)
        self.assertNotEqual(None, self.eng_1.close_date)
        self.assertNotEqual(self.eng_1.open_date, self.eng_1.close_date)

    def test_save_closed_to_pending(self):
        self.eng_1.status = models.Engagement.CLOSED_STATUS
        self.eng_1.save()

        self.eng_1.status = models.Engagement.PENDING_STATUS
        self.eng_1.save()

        self.assertEqual(None, self.eng_1.open_date)
        self.assertEqual(None, self.eng_1.close_date)

    def test_save_closed_to_open(self):
        self.eng_1.status = models.Engagement.CLOSED_STATUS
        self.eng_1.save()

        self.eng_1.status = models.Engagement.OPEN_STATUS
        self.eng_1.save()

        self.assertNotEqual(None, self.eng_1.open_date)
        self.assertEqual(None, self.eng_1.close_date)

    def test_is_pending(self):
        self.eng_1.status = models.Engagement.PENDING_STATUS
        self.eng_1.save()

        self.assertTrue(self.eng_1.is_pending())
        self.assertFalse(self.eng_1.is_open())
        self.assertFalse(self.eng_1.is_closed())

    def test_is_open(self):
        self.eng_1.status = models.Engagement.OPEN_STATUS
        self.eng_1.save()

        self.assertFalse(self.eng_1.is_pending())
        self.assertTrue(self.eng_1.is_open())
        self.assertFalse(self.eng_1.is_closed())

    def test_is_closed(self):
        self.eng_1.status = models.Engagement.CLOSED_STATUS
        self.eng_1.save()

        self.assertFalse(self.eng_1.is_pending())
        self.assertFalse(self.eng_1.is_open())
        self.assertTrue(self.eng_1.is_closed())

    def test_is_ready_for_work(self):
        self.eng_1.status = models.Engagement.PENDING_STATUS
        self.eng_1.start_date = datetime.date.today()
        self.eng_1.save()

        self.assertTrue(self.eng_1.is_ready_for_work())

        self.eng_1.start_date = datetime.date.today() + datetime.timedelta(days=1)
        self.eng_1.save()

        self.assertFalse(self.eng_1.is_ready_for_work())

    def test_is_past_due(self):
        self.eng_1.status = models.Engagement.PENDING_STATUS
        self.eng_1.end_date = datetime.date.today() - datetime.timedelta(days=1)
        self.eng_1.save()

        self.assertTrue(self.eng_1.is_past_due())

        self.eng_1.end_date = datetime.date.today()
        self.eng_1.save()

        self.assertFalse(self.eng_1.is_past_due())

        self.eng_1.status = models.Engagement.OPEN_STATUS
        self.eng_1.end_date = datetime.date.today() - datetime.timedelta(days=1)
        self.eng_1.save()

        self.assertTrue(self.eng_1.is_past_due())

        self.eng_1.end_date = datetime.date.today() + datetime.timedelta(days=1)
        self.eng_1.save()

        self.assertFalse(self.eng_1.is_past_due())


class ActivityTypeTests(TestCase):

    def test_str(self):
        self.at_1 = models.ActivityType(name='Test')
        self.assertEqual('Test', self.at_1.__str__())


class ActivityTests(TestCase):

    def setUp(self):
        self.org_1 = models.Organization(name='Org1')
        self.org_1.save()

        self.app_1 = models.Application(name='App1', organization=self.org_1)
        self.app_1.save()

        now = datetime.date.today()
        self.en_1 = models.Engagement(start_date=now, end_date=now + datetime.timedelta(days=5), application=self.app_1)
        self.en_1.save()

        self.at_1 = models.ActivityType(name='Unittest')
        self.at_1.save()

        self.ac_1 = models.Activity(engagement=self.en_1, activity_type=self.at_1)
        self.ac_1.save()

    def test_str(self):
        self.assertEqual('Unittest', self.ac_1.__str__())

    def test_save_pending_to_open(self):
        self.ac_1.status = models.Activity.PENDING_STATUS
        self.ac_1.save()

        self.ac_1.status = models.Activity.OPEN_STATUS
        self.ac_1.save()

        self.assertNotEqual(None, self.ac_1.open_date)
        self.assertEqual(None, self.ac_1.close_date)
        self.assertTrue(self.ac_1.engagement.is_open())

    def test_save_pending_to_closed(self):
        self.ac_1.status = models.Activity.PENDING_STATUS
        self.ac_1.save()

        self.ac_1.status = models.Activity.CLOSED_STATUS
        self.ac_1.save()

        self.assertNotEqual(None, self.ac_1.open_date)
        self.assertNotEqual(None, self.ac_1.close_date)
        self.assertEqual(self.ac_1.open_date, self.ac_1.close_date)

    def test_save_open_to_pending(self):
        self.ac_1.status = models.Activity.OPEN_STATUS
        self.ac_1.save()

        self.ac_1.status = models.Activity.PENDING_STATUS
        self.ac_1.save()

        self.assertEqual(None, self.ac_1.open_date)
        self.assertEqual(None, self.ac_1.close_date)

    def test_save_open_to_closed(self):
        self.ac_1.status = models.Activity.OPEN_STATUS
        self.ac_1.save()

        self.ac_1.status = models.Activity.CLOSED_STATUS
        self.ac_1.save()

        self.assertNotEqual(None, self.ac_1.open_date)
        self.assertNotEqual(None, self.ac_1.close_date)
        self.assertNotEqual(self.ac_1.open_date, self.ac_1.close_date)

    def test_save_closed_to_pending(self):
        self.ac_1.status = models.Activity.CLOSED_STATUS
        self.ac_1.save()

        self.ac_1.status = models.Activity.PENDING_STATUS
        self.ac_1.save()

        self.assertEqual(None, self.ac_1.open_date)
        self.assertEqual(None, self.ac_1.close_date)

    def test_save_closed_to_open(self):
        self.ac_1.status = models.Activity.CLOSED_STATUS
        self.ac_1.save()

        self.ac_1.status = models.Activity.OPEN_STATUS
        self.ac_1.save()

        self.assertNotEqual(None, self.ac_1.open_date)
        self.assertEqual(None, self.ac_1.close_date)
        self.assertTrue(self.ac_1.engagement.is_open())

    def test_save_close_parent_engagement_solo(self):
        """Tests closing parent engagement with only one child activity."""
        now = datetime.date.today()
        self.en_2 = models.Engagement(start_date=now, end_date=now + datetime.timedelta(days=5), application=self.app_1)
        self.en_2.save()

        self.en_2.status = models.Engagement.OPEN_STATUS
        self.en_2.save()

        self.ac_2 = models.Activity(engagement=self.en_2, activity_type=self.at_1)
        self.ac_2.save()

        self.ac_2.status = models.Activity.OPEN_STATUS
        self.ac_2.save()

        self.ac_2.status = models.Activity.CLOSED_STATUS
        self.ac_2.save()

        self.assertEqual(models.Engagement.CLOSED_STATUS, self.ac_2.engagement.status)

    def test_save_close_parent_engagement_multiple(self):
        """Tests closing parent engagement with multiple child activities."""
        now = datetime.date.today()
        self.en_3 = models.Engagement(start_date=now, end_date=now + datetime.timedelta(days=5), application=self.app_1)
        self.en_3.save()

        self.en_3.status = models.Engagement.OPEN_STATUS
        self.en_3.save()

        self.ac_3 = models.Activity(engagement=self.en_3, activity_type=self.at_1)
        self.ac_3.save()

        self.ac_3.status = models.Activity.OPEN_STATUS
        self.ac_3.save()

        self.ac_4 = models.Activity(engagement=self.en_3, activity_type=self.at_1)
        self.ac_4.save()

        self.ac_4.status = models.Activity.OPEN_STATUS
        self.ac_4.save()

        self.ac_3.status = models.Activity.CLOSED_STATUS
        self.ac_3.save()

        self.assertEqual(models.Engagement.OPEN_STATUS, self.en_3.status)

        self.ac_4.status = models.Activity.CLOSED_STATUS
        self.ac_4.save()

        self.assertEqual(models.Engagement.CLOSED_STATUS, self.en_3.status)

    def test_is_pending(self):
        self.ac_1.status = models.Activity.PENDING_STATUS
        self.ac_1.save()

        self.assertTrue(self.ac_1.is_pending())
        self.assertFalse(self.ac_1.is_open())
        self.assertFalse(self.ac_1.is_closed())

    def test_is_open(self):
        self.ac_1.status = models.Activity.OPEN_STATUS
        self.ac_1.save()

        self.assertFalse(self.ac_1.is_pending())
        self.assertTrue(self.ac_1.is_open())
        self.assertFalse(self.ac_1.is_closed())

    def test_is_closed(self):
        self.ac_1.status = models.Activity.CLOSED_STATUS
        self.ac_1.save()

        self.assertFalse(self.ac_1.is_pending())
        self.assertFalse(self.ac_1.is_open())
        self.assertTrue(self.ac_1.is_closed())

    def test_is_ready_for_work(self):
        self.ac_1.status = models.Activity.PENDING_STATUS
        self.ac_1.save()

        self.ac_1.engagement.start_date = datetime.date.today()
        self.ac_1.engagement.save()

        self.assertTrue(self.ac_1.is_ready_for_work())

        self.ac_1.engagement.start_date = datetime.date.today() + datetime.timedelta(days=1)
        self.ac_1.engagement.save()

        self.assertFalse(self.ac_1.is_ready_for_work())

    def test_is_past_due(self):
        self.ac_1.status = models.Activity.PENDING_STATUS
        self.ac_1.save()

        self.ac_1.engagement.end_date = datetime.date.today() - datetime.timedelta(days=1)
        self.ac_1.engagement.save()

        self.assertTrue(self.ac_1.is_past_due())

        self.ac_1.engagement.end_date = datetime.date.today()
        self.ac_1.engagement.save()

        self.assertFalse(self.ac_1.is_past_due())

        self.ac_1.status = models.Activity.PENDING_STATUS
        self.ac_1.save()

        self.ac_1.engagement.end_date = datetime.date.today() - datetime.timedelta(days=1)
        self.ac_1.engagement.save()

        self.assertTrue(self.ac_1.is_past_due())

        self.ac_1.engagement.end_date = datetime.date.today() + datetime.timedelta(days=1)
        self.ac_1.engagement.save()

        self.assertFalse(self.ac_1.is_past_due())


class CommentTests(TestCase):

    def test_str(self):
        self.user_1 = User.objects.create(username='testy', password='secret', email='testy@noreply.com')
        self.user_1.save()

        self.c_1 = models.Comment(message='Hello World', user=self.user_1)
        self.assertEqual('Hello World', self.c_1.__str__())

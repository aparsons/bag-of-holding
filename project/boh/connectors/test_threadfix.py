from django.test import TestCase

from .threadfix import ThreadFixAPI


class ThreadFixAPITests(TestCase):

    def setUp(self):
        self.host = 'https://192.168.1.126:8443/threadfix/'
        self.api_key = 'DJRQjwFrOfAFf7jz1yKFK0YIVKGv9Cp8utY6IcvyE6w'
        self.verify_ssl = False
        self.timeout = 30

        self.threadfix = ThreadFixAPI(host=self.host, api_key=self.api_key, verify_ssl=self.verify_ssl, timeout=self.timeout)

    def test_list_teams(self):
        pass
        #teams = self.threadfix.list_teams()
        #for team in teams.data:
        #    print(str(team['id']) + ' ' + team['name'] + ' ' + str(team['totalVulnCount']))

    def test_create_team(self):
        pass
        #team = self.threadfix.create_team(name='qwerty')
        #print(team)

    def test_get_team(self):
        pass
        #team = self.threadfix.get_team(7)
        #print(team)

    def test_get_team_by_name(self):
        pass
        #team = self.threadfix.get_team_by_name('qwerty')
        #print(team)

    def test_create_application(self):
        pass
        #application = self.threadfix.create_application(team_id=7, name='TDD App', url='http://localhost/')
        #print(application)

    def test_get_application(self):
        pass
        #application = self.threadfix.get_application(application_id=7)
        #print(application)

    def test_set_application_parameters(self):
        pass
        #application = self.threadfix.set_application_parameters(application_id=7, framework_type='JSP', repository_url='http://whooha.com')
        #print(application)

    def test_list_wafs(self):
        pass
        #wafs = self.threadfix.list_wafs()
        #print(wafs)

    def test_create_waf(self):
        pass
        #waf = self.threadfix.create_waf(name='Test Waffle', waf_type='mod_security')
        #print(waf)

    def test_get_waf(self):
        pass
        #waf = self.threadfix.get_waf(1)
        #print(waf)

    def test_get_waf_rules(self):
        pass
        #rules = self.threadfix.get_waf_rules(1)
        #print(rules)

    def test_get_waf_rules_by_application(self):
        pass
        #rules = self.threadfix.get_waf_rules_by_application(1, 7)
        #print(rules)

    def test_set_application_url(self):
        pass
        #application = self.threadfix.set_application_url(7, 'http://www.example-url.com')
        #print(application)

    def test_set_application_waf(self):
        pass
        #application = self.threadfix.set_application_waf(7, 1)
        #print(application)

    def test_get_vulnerabilities(self):
        vulnerabilities = self.threadfix.get_vulnerabilities(show_closed=True)
        print('\n\n' + vulnerabilities.data_json(True) + '\n\n')
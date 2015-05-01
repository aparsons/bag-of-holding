import json
import requests
import requests.exceptions
import requests.packages.urllib3

from boh import __version__ as version


class ThreadFixAPI(object):
    """An API wrapper to facilitate interactions to and from ThreadFix."""

    def __init__(self, host, api_key, verify_ssl=True, timeout=30, debug=False):
        """Initialize a ThreadFix API instance."""

        self.host = host
        self.api_key = api_key
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self.debug = debug  # Prints request and response information.

        if not self.verify_ssl:
            requests.packages.urllib3.disable_warnings()  # Disabling SSL warning messages if verification is disabled.

    # Team

    def list_teams(self):
        """Retrieves all the teams."""
        return self._request('GET', 'rest/teams')

    def create_team(self, name):
        """Creates a team with the given name."""
        return self._request('POST', '/rest/teams/new', {'name': name})

    def get_team(self, team_id):
        """Retrieves a team using the given team id."""
        return self._request('GET', '/rest/teams/' + str(team_id))

    def get_team_by_name(self, name):
        """Retrieves a team using the given name."""
        return self._request('GET', 'rest/teams/lookup?name=' + str(name))

    # Application

    def create_application(self, team_id, name, url=None):
        """Creates an application under the given team with id of team id."""
        params = {'name': name}
        if url:
            params['url'] = url
        return self._request('POST', 'rest/teams/' + str(team_id) + '/applications/new', params)

    def get_application(self, application_id):
        """Retrieves an application using the given application id."""
        return self._request('GET', 'rest/applications/' + str(application_id))

    def set_application_parameters(self, application_id, framework_type, repository_url):
        """Sets parameters for the Hybrid Analysis Mapping ThreadFix functionality."""
        params = {
            'frameworkType': framework_type,
            'repositoryUrl': repository_url
        }
        return self._request('POST', 'rest/applications/' + str(application_id) + '/setParameters', params)

    def set_application_url(self, application_id, url):
        """Sets the application's URL."""
        return self._request('POST', 'rest/applications/' + str(application_id) + '/addUrl', {'url': url})

    def set_application_waf(self, application_id, waf_id):
        """Sets the application's WAF to the WAF with the specified id."""
        return self._request('POST', 'rest/applications/' + str(application_id) + '/setWaf', {'wafId': waf_id})

    # Findings

    def create_manual_finding(self, application_id, vulnerability_type, description, severity, full_url=None,
                              native_id=None, path=None):
        """
        Creates a manual finding with given properties.
        :param application_id: Application identifier number.
        :param vulnerability_type: Name of CWE vulnerability.
        :param description: General description of the issue.
        :param severity: Severity level from 0-8.
        :param full_url: Absolute URL to the page with the vulnerability.
        :param native_id: Specific identifier for vulnerability.
        :param path: Relative path to vulnerability page.
        """

        params = {
            'isStatic': False,
            'vulnType': vulnerability_type,
            'longDescription': description,
            'severity': severity
        }

        if full_url:
            params['fullUrl'] = full_url
        if native_id:
            params['nativeId'] = native_id
        if path:
            params['path'] = path

        return self._request('POST', 'rest/applications/' + str(application_id) + '/addFinding', params)

    def create_static_finding(self, application_id, vulnerability_type, description, severity, parameter=None,
                              file_path=None, native_id=None, column=None, line_text=None, line_number=None):
        """
        Creates a static finding with given properties.
        :param application_id: Application identifier number.
        :param vulnerability_type: Name of CWE vulnerability.
        :param description: General description of the issue.
        :param severity: Severity level from 0-8.
        :param parameter: Request parameter for vulnerability.
        :param file_path: Location of source file.
        :param native_id: Specific identifier for vulnerability.
        :param column: Column number for finding vulnerability source.
        :param line_text: Specific line text to finding vulnerability.
        :param line_number: Specific source line number to find vulnerability.
        """

        if not parameter and not file_path:
            raise AttributeError('Static findings require either parameter or file_path to be present.')

        params = {
            'isStatic': True,
            'vulnType': vulnerability_type,
            'longDescription': description,
            'severity': severity
        }

        if native_id:
            params['nativeId'] = native_id
        if column:
            params['column'] = column
        if line_text:
            params['lineText'] = line_text
        if line_number:
            params['lineNumber'] = line_number

        return self._request('POST', 'rest/applications/' + str(application_id) + '/addFinding', params)

    def upload_scan(self, application_id, file_path):
        """Uploads and processes the scan."""
        return self._request('POST', 'rest/applications/' + str(application_id) + '/upload', files={'file': open(file_path, 'rb')})

    # WAF

    def list_wafs(self):
        """Retrieves all WAFs in system."""
        return self._request('GET', 'rest/wafs')

    def create_waf(self, name, waf_type):
        """Creates a WAF with the given type."""
        params = {
            'name': name,
            'type': waf_type
        }
        return self._request('POST', 'rest/wafs/new', params)

    def get_waf(self, waf_id):
        """Retrieves WAF using the given WAF id."""
        return self._request('GET', 'rest/wafs/' + str(waf_id))

    def get_waf_rules(self, waf_id):
        """Retrieves all the rules for WAF with the given WAF id."""
        return self.get_waf_rules_by_application(waf_id=waf_id, application_id=-1)

    def get_waf_rules_by_application(self, waf_id, application_id):
        """
        Returns the WAF rule text for one or all of the applications in a WAF. If the application id is -1, it will get
        rules for all apps. If the application is a valid application id, rules will be generated for that application.
        """
        return self._request('GET', 'rest/wafs/' + str(waf_id) + '/rules/app/' + str(application_id))

    def upload_waf_log(self, waf_id, file_path):
        """Uploads and processes a WAF log."""
        return self._request('POST', 'rest/wafs/' + str(waf_id) + '/uploadLog', files={'file': open(file_path, 'rb')})

    # Vulnerabilities

    def get_vulnerabilities(self, teams=None, applications=None, channel_types=None, start_date=None, end_date=None,
                            generic_severities=None, generic_vulnerabilities=None, number_merged=None,
                            number_vulnerabilities=None, parameter=None, path=None, show_open=None, show_closed=None,
                            show_defect_open=None, show_defect_closed=None, show_defect_present=None,
                            show_defect_not_present=None, show_false_positive=None, show_hidden=None):
        """
        Returns filtered list of vulnerabilities.
        :param teams: List of team ids.
        :param applications: List of application ids.
        :param channel_types: List of scanner names.
        :param start_date: Lower bound on scan dates.
        :param end_date: Upper bound on scan dates.
        :param generic_severities: List of generic severity values.
        :param generic_vulnerabilities: List of generic vulnerability ids.
        :param number_merged: Number of vulnerabilities merged from different scans.
        :param number_vulnerabilities: Number of vulnerabilities to return.
        :param parameter: Application input that the vulnerability affects.
        :param path: Path to the web page where the vulnerability was found.
        :param show_open: Flag to show all open vulnerabilities.
        :param show_closed: Flag to show all closed vulnerabilities.
        :param show_defect_open: Flag to show any vulnerabilities with open defects.
        :param show_defect_closed: Flag to show any vulnerabilities with closed defects.
        :param show_defect_present: Flag to show any vulnerabilities with a defect.
        :param show_defect_not_present: Flag to show any vulnerabilities without a defect.
        :param show_false_positive: Flag to show any false positives from vulnerabilities.
        :param show_hidden: Flag to show all hidden vulnerabilities.
        """
        params = {}

        # Build parameter list
        if teams:
            params.update(self._build_list_params('teams', 'id', teams))
        if applications:
            params.update(self._build_list_params('applications', 'id', applications))
        if channel_types:
            params.update(self._build_list_params('channelTypes', 'name', channel_types))
        if start_date:
            params['startDate'] = start_date
        if end_date:
            params['endDate'] = end_date
        if generic_severities:
            params.update(self._build_list_params('genericSeverities', 'intValue', generic_severities))
        if generic_vulnerabilities:
            params.update(self._build_list_params('genericVulnerabilities', 'id', generic_vulnerabilities))
        if number_merged:
            params['numberMerged'] = number_merged
        if number_vulnerabilities:
            params['numberVulnerabilities'] = number_vulnerabilities
        if parameter:
            params['parameter'] = parameter
        if path:
            params['path'] = path
        if show_open:
            params['showOpen'] = show_open
        if show_closed:
            params['showClosed'] = show_closed
        if show_defect_open:
            params['showDefectOpen'] = show_defect_open
        if show_defect_closed:
            params['showDefectClosed'] = show_defect_closed
        if show_defect_present:
            params['showDefectPresent'] = show_defect_present
        if show_defect_not_present:
            params['showDefectNotPresent'] = show_defect_not_present
        if show_false_positive:
            params['showFalsePositive'] = show_false_positive
        if show_hidden:
            params['showHidden'] = show_hidden

        print(params)

        return self._request('POST', 'rest/vulnerabilities', params)

    # Utility

    @staticmethod
    def _build_list_params(param_name, key, values):
        """Builds a list of POST parameters from a list or single value."""
        params = {}
        if hasattr(values, '__iter__'):
            index = 0
            for value in values:
                params[str(param_name) + '[' + str(index) + '].' + str(key)] = str(value)
                index += 1
        else:
            params[str(param_name) + '[0].' + str(key)] = str(values)
        return params

    def _request(self, method, url, params=None, files=None):
        """Common handler for all HTTP requests."""
        if not params:
            params = {}
        params['apiKey'] = self.api_key

        headers = {
            'User-Agent': 'bag-of-holding/' + version,
            'Accept': 'application/json'
        }

        try:
            if self.debug:
                print(method + ' ' + url)
                print(params)

            response = requests.request(method=method, url=self.host + url, params=params, files=files, headers=headers, timeout=self.timeout, verify=self.verify_ssl)

            if self.debug:
                print(response.status_code)
                print(response.text)

            try:
                json_response = response.json()

                message = json_response['message']
                success = json_response['success']
                response_code = json_response['responseCode']
                data = json_response['object']

                return ThreadFixResponse(message=message, success=success, response_code=response_code, data=data)
            except ValueError:
                return ThreadFixResponse(message='JSON response could not be decoded.', success=False)
        except requests.exceptions.SSLError:
            return ThreadFixResponse(message='An SSL error occurred.', success=False)
        except requests.exceptions.ConnectionError:
            return ThreadFixResponse(message='A connection error occurred.', success=False)
        except requests.exceptions.Timeout:
            return ThreadFixResponse(message='The request timed out after ' + str(self.timeout) + ' seconds.', success=False)
        except requests.exceptions.RequestException:
            return ThreadFixResponse(message='There was an error while handling the request.', success=False)


class ThreadFixResponse(object):
    """Container for all ThreadFix API responses, even errors."""

    def __init__(self, message, success, response_code=-1, data=None):
        self.message = message
        self.success = success
        self.response_code = response_code
        self.data = data

    def __str__(self):
        if self.data:
            return str(self.data)
        else:
            return self.message

    def data_json(self, pretty=False):
        """Returns the data as a valid JSON string."""
        if pretty:
            return json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            return json.dumps(self.data)
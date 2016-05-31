# Bag of Holding Releases

## 0.0.6 - 5/15/2016

This release brings several highly requested features. You will find that custom fields can be defined and applied to applications. This functionality was developed so it could easily be applied to other models in the future. Another new piece of functionality is the filtering of metrics so yearly totals can be seen. Enjoy!

*Take note of the new github repository location.*

### What's New

* ASVS Tracking for Applications
* Metrics Filtering By Year
* Custom fields for Applications
* Updated Dependencies
* Various Bugfixes

## 0.0.5 - 4/20/2016

Maintenance release to update dependencies and remove stagnant code. This release serves as preparation for upcoming changes.

### What's New

* Dependencies
  * Numerous dependencies have been updated
* Fixed Python 2 reports bug
* Added simplistic ASVS scoring

## 0.0.4 - 07/24/2015

Minor release with reporting application summary and initial addition of ASVS

## 0.0.3 - 06/26/2015

Our goal for the 0.0.3 release was to improve the metrics and reports. You will also find there is now an API available for use.

### What's New

* Dependencies. The project **requirements.txt** has been updated to require the following additional dependencies:
    * Django - Updated 1.7.7 to 1.8.2
    * django-filter - Updated 0.9.2 to 0.10.0
    * Markdown - Updated 2.6.1 to 2.6.2
    * pytz - Updated 2015.2 to 2015.4
    * requests - Updated 2.6.0 to 2.7.0
    * threadfix-api - New 1.1.1
* Metrics
    * Average Time Per Activity
    * Engagement and Activity Stats
* Reports
    * Engagement Coverage Report
    * ThreadFix Summary Report
* API
    * Applications (including ThreadFix metrics)
    * Organizations
* ThreadFix cron task to pull in metrics daily
* 47 Test Cases
* Model managers to get code more centralized
* Project restructuring for requirements and settings

## 1.0.2 - 04/20/2015

Our goal for the 1.0.2 release was to rework the application list view and add other needed metadata.

### What's New

* Dependencies. The project **requirements.txt** has been updated to require the following additional dependencies:
    * django-filter - Added 0.9.2
    * phonenumbers - Updated 7.0.2 to 7.0.4
    * pytz - Updated 2014.10 to 2015.2
    * requests - Updated 2.5.3 to 2.6.0
* Service Level Agreements can now be applied to applications. This functionality is preliminary. In the future, rules will be able to be applied to the SLAs.
* Regulations can now be applied to applications. The following will be pre-loaded with the migration:
    * 12 Regulations
* Technologies can now be applied to applications. The following will be pre-loaded with the migration:
    * 24 Programming Languages
    * 5 Operating Systems
    * 13 Data Stores
    * 32 Frameworks
    * 5 Third-Party Components
    * 3 Web Servers
    * 7 Application Servers
    * 5 Hosting Providers
    * 4 Denial of Service Protections
    * 5 Firewalls
* Application List View Enhancements
    * Table View
    * Filtering, Search, Pagination, Page Size
    * Responsive!
* A new select form control
* If an activity's status is changed to open, the parent engagement will be opened.
* If all an engagement's activities are closed, the parent engagement will be closed.
* When a new comment is made, the application will redirect to the in-page location of that comment.

## 1.0.1 - 03/30/2015

Our goals for the 1.0.1 release was to finish views for the existing data model. However, we did get in some usability and editing changes. We have gotten some very useful feedback and will be incorporating the suggestions into future releases. Keep the feedback coming and I hope you like version 1.0.1.

*Adam Parsons*

### What's New

* Dependencies. The project **requirements.txt** has been updated to require the following additional dependencies:
    * Django 1.7.7 - Updated due to [security issues](https://www.djangoproject.com/weblog/2015/mar/18/security-releases/)
    * django-debug-toolbar - Adds a toolbar used to debug during development
    * html5lib - django-debug-toolbar dependancy
    * six - django-debug-toolbar dependancy
    * sqlparse - django-debug-toolbar dependancy
    * Markdown - Markdown rendering
    * Pygments - Code highlighting
    * phonenumbers - Phone number formatting
* Team Dashboard optimizations
    * Collapsing users, engagement lists
    * Activities colored by status
    * SQL query optimizations
* An example chart was added to metrics
* People can now be added to applications and organizations
    * People can now be marked as application owners and/or emergency contacts.
* Users can now edit their profile and change their own passwords.
* Staff users can now manage application tags, activity types, and services.
    * Staff can now import applications from ThreadFix
* Applications created within the last seven days will be marked as new
* Tags now have descriptions that will show up in tooltips
* Some text fields now accept markdown. These fields will use a special editor to help simplify the syntax.
* Frontend dependencies are now being managed by Bower and compiled using Gulp.
* Version information will show up in the footer after login.

### Known Issues

* Users cannot edit or delete their own comments without using the django admin
* Users have no way to reset their own passwords

Full functionality for some features are not available through the web interface. Until this is fixed you can edit the data using the **Django Site Admin** found on the **Manage** page. The features missing are listed below:

* User management
* Data element management

Not all form fields have a description describing their purpose. These will be improved over time but if you find a particular field menacing please let us know so we can prioritize clarifying its purpose.

*If you run into any issues please report it so we can fix it!*


## 1.0.0 - 03/18/2015

Getting this first release out the door has been a journey. Three months ago this application was just an idea and now... here it is. This project means a lot to me personally. For one to two years before writing this software, I had prototyped numerous similar softwares -- Matt Brown can attest to this. I feel this application takes the best of what I attempted to accomplish and puts it all into one *bag*.

Thank you everyone who inspired, provided feedback, and contributed to this project.

*Adam Parsons*

### What's New

**Everything!** At a high-level, within the application you can do the following:

  * Manage software applications
    * Track important metadata information for future reference
    * Retain application environment URLs, credentials, and notes
    * Classify data elements stored within the application
    * Relate the application to a ThreadFix service.
  * Conduct application engagements and activities
    * Assign activities to users
    * Provide comments on an engagement or activity
  * Review engagements and activities through personal and team dashboards

### Known Issues

Full functionality for some features are not available through the web interface. Until this is fixed you can edit the data using the **Django Site Admin** found on the **Manage** page. The features missing are listed below:

  * User account settings
    * Password Change
    * User Profile
  * Manage settings
  * People
    * CRUD Views
    * Relation to Organizations
    * Relation to Applications

Not all form fields have a description describing their purpose. These will be improved over time but if you find a particular field menacing please let us know so we can prioritize clarifying its purpose.

*If you run into any issues please report it so we can fix it!*

from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from boh.models import Application, EngagementRequestComment, EngagementRequestSubscription, Person

from . import models


class EmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        """Validates email must end with @pearson.com"""
        email = self.cleaned_data['email'].lower()
        if not email.endswith('@pearson.com'):
            raise forms.ValidationError('Your email address must end with @pearson.com')
        return email


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'phone_work', 'phone_mobile', 'job_title', 'role']


class ApplicationForm(forms.Form):
    application = forms.ModelChoiceField(queryset=Application.objects.requestable(), help_text=mark_safe(_('Don\'t see your application in this list? Let us know at <a href="mailto:appsec@pearson.com">appsec@pearson.com</a>')))
    version = forms.CharField(max_length=64)
    service_bundle = forms.ModelChoiceField(queryset=models.ServiceBundle.objects.all(), help_text=_('See the table below for more information.'))


class AppScanForm(forms.Form):
    location = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    credentials = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    peroot_name = forms.CharField(max_length=16, help_text=_('Access to the AppScan Enterprise console will be provided.'))
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)


class AppScanRetestForm(forms.Form):
    # TODO
    pass


class SourceCodeForm(forms.Form):  # Abstract
    GIT_REPOSITORY = 'git'
    PERFORCE_REPOSITORY = 'perforce'
    SVN_REPOSITORY = 'svn'
    TFS_REPOSITORY = 'tfs'
    OTHER_REPOSITORY = 'other'
    REPOSITORY_TYPE_CHOICES = (
        (GIT_REPOSITORY, 'Git'),
        (PERFORCE_REPOSITORY, 'Perforce'),
        (SVN_REPOSITORY, 'Subversion (SVN)'),
        (TFS_REPOSITORY, 'Team Foundation Server (TFS)'),
        (OTHER_REPOSITORY, 'Other')
    )

    repository_type = forms.MultipleChoiceField(choices=REPOSITORY_TYPE_CHOICES)
    location = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))


class CheckMarxForm(SourceCodeForm):
    email = forms.EmailField(help_text=_('Access to the Checkmarx web interface will be provided.'))
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)


class VeracodeForm(SourceCodeForm):
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)


class ConfirmForm(forms.Form):
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)

"""
- Requestor Info
- Application
- Application Description

- Metadata
  - Platform
  - Lifecycle (Optional)
  - Origin
  - Criticality

- Technologies (Optional)
- Regulations (Optional)

- Activities

- Availablity Date Window
- Project deadline (Optional)

- Status: Recieved, Waiting for Response, Declined, Approved (Readonly),

- Remarks

- Software Version? (Optional)
Manual Assessment
AppScan Setup
Checkmarx
 - Source Code Repository
Veracode
"""


class EngagementRequestCommentForm(forms.ModelForm):
    class Meta:
        model = EngagementRequestComment
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3})
        }


class EngagementRequestSubscriptionSettingsForm(forms.ModelForm):
    class Meta:
        model = EngagementRequestSubscription
        fields = ['send_status_updates', 'send_comments']


class EngagementRequestSubscriptionDeleteForm(forms.ModelForm):
    class Meta:
        model = EngagementRequestSubscription
        fields = []

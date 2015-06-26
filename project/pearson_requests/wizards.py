from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from formtools.wizard.views import SessionWizardView

from boh import models

from . import forms


def show_person_from_condition(wizard):
    """Show the person form if no person is found with the supplied email address."""
    cleaned_data = wizard.get_cleaned_data_for_step(ExternalRequestWizard.EMAIL_STEP)
    if cleaned_data:
        email = cleaned_data['email'].lower()
        try:
            person = models.Person.objects.get(email=email)
            return False
        except ObjectDoesNotExist:
            return True



class ExternalRequestWizard(SessionWizardView):

    EMAIL_STEP = 'email'
    PERSON_STEP = 'person'
    APPLICATION_STEP = 'application'
    CONFIRM_STEP = 'confirm'

    Forms = [
        (EMAIL_STEP, forms.EmailForm),
        (PERSON_STEP, forms.PersonForm),
        (APPLICATION_STEP, forms.ApplicationForm),
        (CONFIRM_STEP, forms.ConfirmForm)
    ]

    Templates = {
        EMAIL_STEP: 'pearson_requests/wizards/external_request/email.html',
        PERSON_STEP: 'pearson_requests/wizards/external_request/person.html',
        APPLICATION_STEP: 'pearson_requests/wizards/external_request/application.html',
        CONFIRM_STEP: 'pearson_requests/wizards/external_request/confirmation.html'
    }

    Conditions = {
        PERSON_STEP: show_person_from_condition
    }

    def get_form_initial(self, step):

        if step is ExternalRequestWizard.PERSON_STEP:
            cleaned_data = self.get_cleaned_data_for_step(ExternalRequestWizard.EMAIL_STEP)
            if cleaned_data:
                return self.instance_dict.get(step, {'email': cleaned_data['email']})

        return self.instance_dict.get(step, None)

    def get_template_names(self):
        return [ExternalRequestWizard.Templates[self.steps.current]]

    def done(self, form_list, **kwargs):
        # Process form
        for form in form_list:
            print(form.cleaned_data)
        return HttpResponseRedirect(reverse('pearson_requests:external_request_success'))

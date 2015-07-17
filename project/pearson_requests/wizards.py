from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response

from formtools.wizard.views import SessionWizardView

from boh.models import Application, Person

from . import forms
from . import models


def show_person_from_condition(wizard):
    """Show the person form if no person is found with the supplied email address."""
    cleaned_data = wizard.get_cleaned_data_for_step(ExternalRequestWizard.EMAIL_STEP)
    if cleaned_data:
        email = cleaned_data['email'].lower()
        try:
            person = Person.objects.get(email=email)
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

    def get_person(self, email):
        """Returns a Person object or looks up the person with the specified email address."""
        data = self.get_cleaned_data_for_step(ExternalRequestWizard.PERSON_STEP)
        return

    def get_context_data(self, form, **kwargs):
        context = super(ExternalRequestWizard, self).get_context_data(form=form, **kwargs)
        context.update({'service_bundles': models.ServiceBundle.objects.all()})

        if self.steps.current is ExternalRequestWizard.CONFIRM_STEP:
            email_data = self.get_cleaned_data_for_step(ExternalRequestWizard.EMAIL_STEP)
            person_data = self.get_cleaned_data_for_step(ExternalRequestWizard.PERSON_STEP)
            if person_data:
                person = Person(
                    first_name=person_data['first_name'],
                    last_name=person_data['last_name'],
                    email=person_data['email'],
                    role=person_data['role'],
                    job_title=person_data['job_title'],
                    phone_work=person_data['phone_work'],
                    phone_mobile=person_data['phone_mobile'],
                )
            else:
                person = Person.objects.get(email=email_data['email'])
            context.update({'person_data': person})

            application_data = self.get_cleaned_data_for_step(ExternalRequestWizard.APPLICATION_STEP)
            context.update({'application_data': application_data})
        return context

    def get_form_initial(self, step):
        # Sets the email address from the email step
        if step is ExternalRequestWizard.PERSON_STEP:
            cleaned_data = self.get_cleaned_data_for_step(ExternalRequestWizard.EMAIL_STEP)
            if cleaned_data:
                return self.instance_dict.get(step, {'email': cleaned_data['email']})

        return self.instance_dict.get(step, None)

    def get_template_names(self):
        return [ExternalRequestWizard.Templates[self.steps.current]]

    def done(self, form_list, **kwargs):
        # Process form
        return render_to_response('pearson_requests/wizards/external_request/success.html', {
            'form_data': [form.cleaned_data for form in form_list]
        })

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render_to_response

from formtools.wizard.views import SessionWizardView

from boh.models import Person, EngagementRequest

from . import forms, models


def show_person_form_condition(wizard):
    """Show the person form if no person is found with the supplied email address."""
    cleaned_data = wizard.get_cleaned_data_for_step(ServiceRequestWizard.EMAIL_STEP)
    if cleaned_data:
        email = cleaned_data['email'].lower()
        try:
            person = Person.objects.get(email=email)
            return False
        except ObjectDoesNotExist:
            return True
    else:
        return True


def show_appscan_form_condition(wizard):
    """Shows the AppScan form if enabled in service bundle."""
    cleaned_data = wizard.get_cleaned_data_for_step(ServiceRequestWizard.APPLICATION_STEP)
    if cleaned_data:
        return cleaned_data['service_bundle'].show_appscan_form
    else:
        return False


def show_checkmarx_form_condition(wizard):
    """Shows the Checkmarx form if enabled in the service bundle."""
    cleaned_data = wizard.get_cleaned_data_for_step(ServiceRequestWizard.APPLICATION_STEP)
    if cleaned_data:
        return cleaned_data['service_bundle'].show_checkmarx_form
    else:
        return False


class ServiceRequestWizard(SessionWizardView):
    EMAIL_STEP = 'email'
    PERSON_STEP = 'person'
    APPLICATION_STEP = 'application'
    APPSCAN_STEP = 'appscan'
    CHECKMARX_STEP = 'checkmarx'
    CONFIRM_STEP = 'confirm'

    Forms = [
        (EMAIL_STEP, forms.EmailForm),
        (PERSON_STEP, forms.PersonForm),
        (APPLICATION_STEP, forms.ApplicationForm),
        (APPSCAN_STEP, forms.AppScanForm),
        (CHECKMARX_STEP, forms.CheckMarxForm),
        (CONFIRM_STEP, forms.ConfirmForm),
    ]

    Templates = {
        EMAIL_STEP: 'pearson_requests/wizards/external_request/email.html',
        PERSON_STEP: 'pearson_requests/wizards/external_request/person.html',
        APPLICATION_STEP: 'pearson_requests/wizards/external_request/application.html',
        APPSCAN_STEP: 'pearson_requests/wizards/external_request/appscan.html',
        CHECKMARX_STEP: 'pearson_requests/wizards/external_request/checkmarx.html',
        CONFIRM_STEP: 'pearson_requests/wizards/external_request/confirmation.html',
    }

    Conditions = {
        PERSON_STEP: show_person_form_condition,
        APPSCAN_STEP: show_appscan_form_condition,
        CHECKMARX_STEP: show_checkmarx_form_condition,
    }

    def get_context_data(self, form, **kwargs):
        context = super(ServiceRequestWizard, self).get_context_data(form=form, **kwargs)
        context.update({'active_top': 'requests'})
        context.update({'service_bundles': models.ServiceBundle.objects.all()})

        if self.steps.current is ServiceRequestWizard.CONFIRM_STEP:
            email_data = self.get_cleaned_data_for_step(ServiceRequestWizard.EMAIL_STEP)
            person_data = self.get_cleaned_data_for_step(ServiceRequestWizard.PERSON_STEP)
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

            application_data = self.get_cleaned_data_for_step(ServiceRequestWizard.APPLICATION_STEP)
            context.update({'application_data': application_data})
        return context

    def get_form_initial(self, step):
        # Sets the email address from the email step
        if step is ServiceRequestWizard.PERSON_STEP:
            cleaned_data = self.get_cleaned_data_for_step(ServiceRequestWizard.EMAIL_STEP)
            if cleaned_data:
                return self.instance_dict.get(step, {'email': cleaned_data['email']})

        return self.instance_dict.get(step, None)

    def get_template_names(self):
        return [ServiceRequestWizard.Templates[self.steps.current]]

    def done(self, form_list, **kwargs):
        email_data = self.get_cleaned_data_for_step(ServiceRequestWizard.EMAIL_STEP)

        # Create person if they do not exist
        person_data = self.get_cleaned_data_for_step(ServiceRequestWizard.PERSON_STEP)
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
            person.save()
        else:
            try:
                person = Person.objects.get(email=email_data['email'])
            except Person.DoesNotExist:
                raise Http404("Person does not exist")

        application_data = self.get_cleaned_data_for_step(ServiceRequestWizard.APPLICATION_STEP)

        appscan_data = self.get_cleaned_data_for_step(ServiceRequestWizard.APPSCAN_STEP)
        checkmarx_data = self.get_cleaned_data_for_step(ServiceRequestWizard.CHECKMARX_STEP)

        # Aggregate description
        description = "nothing yet"

        import uuid

        # Create new service request
        request = EngagementRequest.objects.create(
            name=application_data['service_bundle'].name,
            description=description,
            version=application_data['version'],
            requester=person,
            application=application_data['application']
        )

        for activity_type in application_data['service_bundle'].activities.all():
            request.activity_types.add(activity_type)

        request.save()

        # TODO - Fix Broken - Make sure to create a new subscriber and add the token to the response

        # TODO Send two emails

        return render_to_response('pearson_requests/wizards/external_request/success.html', {
            'person': person,
            'token': request.token
        })

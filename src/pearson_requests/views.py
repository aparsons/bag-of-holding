import random

from django.contrib import messages
from django.contrib.auth import get_user
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_http_methods

from boh.models import EngagementRequestSubscription

from boh.views import error_messages, success_messages

from . import forms


@require_http_methods(['GET'])
def success(request):
    return render(request, 'pearson_requests/wizards/external_request/success.html')


@require_http_methods(['GET'])
def status(request, token):
    subscription = get_object_or_404(EngagementRequestSubscription, token=token, active=True)

    subscription_settings_form = forms.EngagementRequestSubscriptionSettingsForm(instance=subscription)
    subscription_delete_form = forms.EngagementRequestSubscriptionDeleteForm(instance=subscription)

    comment_form = forms.EngagementRequestCommentForm()

    return render(request, 'pearson_requests/status.html', {
        'subscription': subscription,
        'engagement_request': subscription.engagement_request,
        'subscription_settings_form': subscription_settings_form,
        'subscription_delete_form': subscription_delete_form,
        'comment_form': comment_form
    })


@require_http_methods(['POST'])
def status_settings(request, token):
    subscription = get_object_or_404(EngagementRequestSubscription, token=token, active=True)

    subscription_settings_form = forms.EngagementRequestSubscriptionSettingsForm(request.POST, instance=subscription)

    if subscription_settings_form.is_valid():
        subscription_settings_form.save()
        messages.success(request, _('Your subscription settings have been successfully updated.'), extra_tags=random.choice(success_messages))
    else:
        messages.error(request, _('There was a problem updating your subscription settings.'), extra_tags=random.choice(error_messages))

    return redirect('pearson_requests:status', subscription.token)


@require_http_methods(['POST'])
def status_comment(request, token):
    subscription = get_object_or_404(EngagementRequestSubscription, token=token, active=True)

    comment_form = forms.EngagementRequestCommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.engagement_request = subscription.engagement_request

        if request.user.is_authenticated():
            comment.user = request.user
        else:
            comment.subscription = subscription

        comment.save()
        messages.success(request, _('Your comment has been successfully published.'), extra_tags=random.choice(success_messages))
    else:
        messages.error(request, _('There was a problem publishing your comment.'), extra_tags=random.choice(error_messages))

    print(comment_form.errors)

    return redirect('pearson_requests:status', subscription.token)


@require_http_methods(['POST'])
def status_cancel(request, token):
    subscription = get_object_or_404(EngagementRequestSubscription, token=token, active=True)

    subscription_delete_form = forms.EngagementRequestSubscriptionDeleteForm(request.POST, instance=subscription)

    if subscription_delete_form.is_valid():
        subscription.active = False
        subscription.save()
        messages.success(request, _('Your subscription has been successfully cancelled.'), extra_tags=random.choice(success_messages))
        return redirect('pearson:index')
    else:
        messages.error(request, _('There was a problem cancelling your subscription.'), extra_tags=random.choice(error_messages))
        return redirect('pearson_requests:status', subscription.token)

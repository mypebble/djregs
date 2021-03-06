from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import CharField, TextField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from registration.models import RegistrationProfile


def _get_user_search_fields():
    """Get the list of search fields to give to the admin site.
    """
    User = get_user_model()

    fieldset = [
        f.name
        for f in User._meta.get_fields()
        if isinstance(f, (CharField, TextField))]
    return [u'user__{}'.format(f) for f in fieldset]


class RegistrationAdmin(admin.ModelAdmin):
    actions = ['activate_users', 'resend_activation_email']
    list_display = ('user', 'activation_key_expired')
    raw_id_fields = ['user']
    search_fields = _get_user_search_fields()

    def activate_users(self, request, queryset):
        """
        Activates the selected users, if they are not alrady
        activated.

        """
        for profile in queryset:
            RegistrationProfile.objects.activate_user(profile.activation_key)
    activate_users.short_description = _("Activate users")

    def resend_activation_email(self, request, queryset):
        """
        Re-sends activation emails for the selected users.

        Note that this will *only* send activation emails for users
        who are eligible to activate; emails will not be sent to users
        whose activation keys have expired or who have already
        activated.

        """
        site = get_current_site(request)

        for profile in queryset:
            if not profile.activation_key_expired():
                profile.send_activation_email(site)
    resend_activation_email.short_description = _("Re-send activation emails")


admin.site.register(RegistrationProfile, RegistrationAdmin)

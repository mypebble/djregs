"""
Forms and validation code for user registration.

Note that all of these forms assume Django's bundle default ``User``
model; since it's not possible for a form to anticipate in advance the
needs of custom user models, you will need to write your own forms if
you're using a custom model.

"""
from django.contrib.auth.models import User, get_user_model
from django import forms
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.

    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """
    required_css_class = 'required'

    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                label=_("Username"),
                                error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    email = forms.EmailField(label=_("E-mail"))
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password (again)"))

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data


class RegistrationFormTermsOfService(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.

    """
    tos = forms.BooleanField(widget=forms.CheckboxInput,
                             label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={'required': _("You must agree to the terms to register")})


class RegistrationFormUniqueEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.

    """
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']


class RegistrationFormNoFreeEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which disallows registration with
    email addresses from popular free webmail services; moderately
    useful for preventing automated spam registrations.

    To change the list of banned domains, subclass this form and
    override the attribute ``bad_domains``.

    """
    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com',
                   'yahoo.com']

    def clean_email(self):
        """
        Check the supplied email address against a list of known free
        webmail domains.

        """
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in self.bad_domains:
            raise forms.ValidationError(_("Registration using free email addresses is prohibited. Please supply a different email address."))
        return self.cleaned_data['email']


class CustomRegistrationForm(forms.ModelForm):
    """Register a user in a system that uses Django's Custom User Models.
    As in the RegistrationForm, don't define save(), as our RegistrationViews
    handle that stuff.
    """
    password1 = forms.CharField(
        widget=forms.PasswordInput, label=_("Password"))
    password2 = forms.CharField(
        widget=forms.PasswordInput, label=_("Password (again)"))

    class Meta:
        model = get_user_model()
        exclude = ('password',)

    def clean(self):
        """Ensure our username field is unique.
        You need to call this in any subclasses.
        """
        cleaned_data = self.cleaned_data
        model = self._meta.model
        username_field = model.USERNAME_FIELD

        username = cleaned_data[username_field]

        query = {
            username_field: username,
        }

        user_exists = model.objects.filter(**query).exists()

        if user_exists:
            _msg = "A user with that {0} already exists.".format(
                username_field)
            self._errors[username_field] = self.error_class([_(_msg)])
            del cleaned_data[username_field]

        return cleaned_data

    def save(self):
        """Do not save.
        """
        raise NotImplementedError("This shouldn't be called")


class ActivationResendForm(forms.Form):
    """Form for re-sending the Activation Email.
    """
    email = forms.EmailField(
        label=_('Your email address'), required=True)

    def clean_email(self):
        """Checks to see if the email address exists and is an inactive user.
        If it is, returns that user.
        """
        email = self.cleaned_data['email']

        try:
            user = User.objects.get(
                email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(_(
                u"I'm sorry but we don't recognise this email address. Have "
                "you signed up?"))

        if user.is_active:
            raise forms.ValidationError(_(
                u"Your email address has already been validated. Have you "
                u"forgotten your password?"))

        return user

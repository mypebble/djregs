from django.conf import settings
from django.contrib.auth.models import User
try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse
    
from django.test import TestCase

from registration.forms import RegistrationForm


class SimpleBackendViewTests(TestCase):
    urls = 'registration.backends.simple.urls'

    def test_allow(self):
        """
        The setting ``REGISTRATION_OPEN`` appropriately controls
        whether registration is permitted.
        
        """
        old_allowed = getattr(settings, 'REGISTRATION_OPEN', True)
        settings.REGISTRATION_OPEN = True

        resp = self.client.get(reverse('registration_register'))
        self.assertEqual(200, resp.status_code)

        settings.REGISTRATION_OPEN = False

        # Now all attempts to hit the register view should redirect to
        # the 'registration is closed' message.
        resp = self.client.get(reverse('registration_register'))
        self.assertRedirects(resp, reverse('registration_disallowed'))
        
        resp = self.client.post(reverse('registration_register'),
                                data={'username': 'bob',
                                      'email': 'bob@example.com',
                                      'password1': 'secret',
                                      'password2': 'secret'})
        self.assertRedirects(resp, reverse('registration_disallowed'))

        settings.REGISTRATION_OPEN = old_allowed

    def test_registration_get(self):
        """
        HTTP ``GET`` to the registration view uses the appropriate
        template and populates a registration form into the context.
        
        """
        resp = self.client.get(reverse('registration_register'))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp,
                                'registration/registration_form.html')
        self.failUnless(isinstance(resp.context['form'],
                        RegistrationForm))

    def test_registration(self):
        """
        Registration creates a new account and logs the user in.

        """
        resp = self.client.post(reverse('registration_register'),
                                data={'username': 'bob',
                                      'email': 'bob@example.com',
                                      'password1': 'secret',
                                      'password2': 'secret'})

        self.assertEqual(302, resp.status_code)
        self.failUnless('/registration/register/complete/' in resp['Location'])

        new_user = User.objects.get(username='bob')
        
        self.failUnless(new_user.check_password('secret'))
        self.assertEqual(new_user.email, 'bob@example.com')
        
        self.failIfEqual(new_user.is_active, True)

        url = reverse(
            'registration_activate', 
            kwargs={'activation_key':new_user.registrationprofile.activation_key}
        ) 
        
        resp = self.client.get(url)
        
        self.assertEqual(302, resp.status_code)

        # Reload after activation_key is sent
        user = User.objects.get(username='bob')
        # New user must be active.
        self.failUnless(user.is_active)
        

    def test_registration_failure(self):
        """
        Registering with invalid data fails.
        
        """
        resp = self.client.post(reverse('registration_register'),
                                data={'username': 'bob',
                                      'email': 'bob@example.com',
                                      'password1': 'secret',
                                      'password2': 'notsecret'})
        self.assertEqual(200, resp.status_code)
        self.failIf(resp.context['form'].is_valid())

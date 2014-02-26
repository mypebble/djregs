from django.conf import settings
from django.contrib.auth.models import get_user_model

from registration import signals
from registration.forms import CustomRegistrationForm
from registration.views import RegistrationView as BaseRegistrationView


class RegistrationView(BaseRegistrationView):
    """A registration backend that implements a workflow for users that want to
    create their own custom user model.
    This most closely resembles the simple backend, since custom users will
    likely have a lot of logic that is outside the scope for this backend.
    """
    form_class = CustomRegistrationForm
    model = get_user_model()

    def register(self, request, **cleaned_data):
        """Register the user.
        """
        username_field = self.model.USERNAME_FIELD

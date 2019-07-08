from django.conf.urls import include, url

from django.contrib import admin
import registration.urls as registration_urls 

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'custom_user_tests.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^registration/', include(registration_urls.urlpatterns))
]

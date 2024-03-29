"""SFIAGenerator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dynamic_preferences.models import GlobalPreferenceModel
from django.conf import settings
# Removing the global preferences from the admin dashboard so they can only be changed using the language preferences form page
# This must be done here as if you try to do it from admin.py it will not yet have been registered and will throw an error
admin.autodiscover()
# Only execute this line if DEBUG is false, as it will surpress other errors if django tries to unregister the model before it has been registered (due to an error)
if not settings.DEBUG:
    admin.site.unregister(GlobalPreferenceModel)

urlpatterns = [
    path('', include('Generator.urls')),
    path('admin/', admin.site.urls),
	path('i18n/', include('django.conf.urls.i18n')),
]

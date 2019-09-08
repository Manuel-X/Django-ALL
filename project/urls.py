"""project URL Configuration

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
from django.urls import path,include

from django.conf import settings           # import settings file to import static function
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    #namespace allows same url name in different apps
    # app_name variable should be defined in url file of app
    # namespace should be added before all urls
    path('app/', include('app.urls', namespace='app')),  
]

# += as it adds newly added files in static folder
# STATIC_URL defined in settings
# STATIC_ROOT defined in settings
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT) 
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 

'''
static folder is created inside app and contains: 
1) css style sheet(custom.css)
2) js style sheet(custom.js)
3) images (logos, background images and banners)
'''


from django.contrib import admin
from .models import Store,Item   #import Store mode to register it in admin page

# Register your models here.

admin.site.register(Store)  #register Store model in admin page
admin.site.register(Item)  #register Store model in admin page
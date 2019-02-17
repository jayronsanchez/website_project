from django.contrib import admin
from inventory import models
# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Item)

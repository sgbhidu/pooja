from django.contrib import admin
from .models import permanent_Address,app_users,saved_Address,color_quantity,pooja_products
# Register your models here.
from django.apps import apps
models = apps.get_models()

admin.site.register(permanent_Address)
admin.site.register(saved_Address)
admin.site.register(app_users)

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
from django.contrib import admin
from django.apps import apps


for app in [apps.get_app_config('main'), apps.get_app_config('student'), apps.get_app_config('academic') ]:
	for model_name, model in app.models.items():
	    admin.site.register(model)
from django.contrib import admin
from django.apps import apps


_apps = []
labels = ['main', 'student', 'academic', 'library', 'transport',  'accounting']
for l in labels:
	_apps.append(apps.get_app_config(l))

for app in _apps:
	for model_name, model in app.models.items():
	    admin.site.register(model)
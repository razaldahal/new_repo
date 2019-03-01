from rest_framework import routers
from django.urls import include,path
from django.conf.urls import url
from .views import *
router = routers.DefaultRouter()

router.register('institution',InstitutuionDetailsViewset)

urlpatterns=[
	url(r'logo', CollegeLogo.as_view(), name='college-logo'),
	path('',include(router.urls)),
]
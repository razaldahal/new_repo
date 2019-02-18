from rest_framework import routers
from django.urls import include,path
from django.conf.urls import url
from .views import InstitutuionDetailsViewset
router = routers.DefaultRouter()
router.register('institution',InstitutuionDetailsViewset)

urlpatterns=[
	path('',include(router.urls)),
]

from django.urls import path,include
from django.conf.urls import url
from django.conf.urls import url
from rest_framework import routers
from rest_framework_nested import routers


from .views import *

router = routers.SimpleRouter()

router.register(r'admission', StudentAdmissionViewSet)
router.register(r'', StudentViewSet)


urlpatterns = [
	url(r'search', StudentSearchViewSet.as_view(), name='student-search'),

	url(r'^', include(router.urls)),

]
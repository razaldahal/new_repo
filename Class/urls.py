from django.urls import path,include
from rest_framework import routers
from Class import views

router = routers.DefaultRouter()
router.register('',views.ClassViewSet)

urlpatterns=[
	path('',include(router.urls))
]
from django.urls import path,include
from rest_framework import routers

from guardain import views

router = routers.DefaultRouter()
#router.register('',views.GuardianViewSet)

urlpatterns =[
	path('',include(router.urls)),
]
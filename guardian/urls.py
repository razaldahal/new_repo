from django.urls import path,include
from rest_framework import routers

from guardian import views

router = routers.DefaultRouter()
router.register('guardian',views.GuardianViewSet)
router.register('guardian_student',views.GuardianStudentViewSet)

urlpatterns =[
	path('',include(router.urls)),
]
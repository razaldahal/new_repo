from django.urls import path,include
from rest_framework import routers

from admission import views

router = routers.DefaultRouter()
router.register(r'student',views.StudentAdmissionViewSet)

urlpatterns = [
	path('',include(router.urls)),

	]
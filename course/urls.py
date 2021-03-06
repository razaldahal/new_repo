from django.urls import path,include
from rest_framework import routers

from course import views

router = routers.SimpleRouter()
router.register('school',views.SchoolViewset)
router.register('department',views.DepartmentViewset)
router.register('course',views.CourseViewSet)
router.register('batch',views.BatchViewSet)

urlpatterns = [
	path('',include(router.urls))
]
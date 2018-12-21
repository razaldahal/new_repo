from django.urls import path,include
from rest_framework import routers

from student import views

router = routers.DefaultRouter()
router.register('assignment',views.StudentAssignmentViewSt)
router.register('test',views.TestStudentViewSet)
router.register('',views.StudentGetViewSet)


urlpatterns = [
	path('',include(router.urls))
]
from django.urls import path,include

from rest_framework import routers

from teacher import views

router = routers.DefaultRouter()
router.register('addsubject',views.SubjectViewSet)
router.register('assignment',views.AssignmentViewSet)
router.register('resources',views.ResourcesViewSet)
router.register('test',views.TestViewSet)
router.register('',views.TeacherViewSet)

urlpatterns = [
	path('',include(router.urls))
	]
from django.urls import path,include
from rest_framework import routers

from course import views

router = routers.SimpleRouter()
router.register('school',views.SchoolViewset)
router.register('department',views.DepartmentViewset)
router.register('course',views.CourseViewSet)
router.register('batch',views.BatchViewSet)
router.register('assignsubject',views.AssignSubjectViewset)
router.register('subjectallocation',views.SubjectAllocationViewset)
router.register('electivesubject',views.ElectiveSubjectViewset)

urlpatterns = [
	path('',include(router.urls))
]
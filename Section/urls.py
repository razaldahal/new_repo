from django.urls import path,include
from rest_framework import routers
from Section import views

router = routers.DefaultRouter()
router.register('student',views.SectionStudentViewSet)
router.register('teacher',views.TeacherSectionViewSet)
router.register('routine',views.SectionRoutineViewSet)

router.register('',views.SectionViewSet)


urlpatterns=[
	path('',include(router.urls)),
]
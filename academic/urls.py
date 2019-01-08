from django.urls import path,include
from django.conf.urls import url
from rest_framework import routers
from rest_framework_nested import routers


from .views import *

router = routers.SimpleRouter()

router.register('year', AcademicYearViewSet)
router.register(r'course', CourseViewSet)
router.register(r'class', ClassViewSet)

course_router = routers.NestedSimpleRouter(router, r'course', lookup='course')
course_router.register(r'class', CourseClassViewSet, base_name='course-class')

class_router = routers.NestedSimpleRouter(router, r'class', lookup='class')
class_router.register(r'section', ClassSectionViewSet, base_name='class-section')


urlpatterns = [
	path('',include(class_router.urls)),
	path('',include(course_router.urls)),
	url(r'^', include(router.urls)),
]
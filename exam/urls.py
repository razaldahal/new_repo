from rest_framework.routers import DefaultRouter
from exam import views
from django.urls import include,path
from rest_framework_nested import routers
from course.views import CourseViewSet
from Class.views import ClassViewSet
from django.conf.urls import url
from .views import *
from Section.views import SectionViewSet

router = routers.SimpleRouter()


router.register(r'course', CourseViewSet)
router.register(r'class', ClassViewSet)
router.register(r'section',SectionViewSet)

course_router = routers.NestedSimpleRouter(router, r'course', lookup='course')
course_router.register(r'class', CourseClassViewSet, base_name='course-class')

class_router = routers.NestedSimpleRouter(router, r'class', lookup='class')
class_router.register(r'section', ClassSectionViewSet, base_name='class-section')

section_router=routers.NestedSimpleRouter(router,r'section',lookup='section')
section_router.register(r'subject',SectionsubjectViewSet,base_name='section-subject')
section_router.register(r'student',SectionstdViewSet,base_name='section-student')


router.register('term',views.TermViewset)
router.register('schedule',views.ScheduleViewset)
router.register('addmarks',views.AddMarksViewSet)
router.register('studentmarks',views.StudentmarksViewSet)
router.register('sectionsubject',views.SectionSubjectViewSet)
router.register('sectionstudent',views.SectionstdViewSet)
urlpatterns = [
	path('',include(class_router.urls)),
	path('',include(course_router.urls)),
	path('',include(section_router.urls)),
	path('',include(router.urls)),
	url(r'^', include(router.urls))
]







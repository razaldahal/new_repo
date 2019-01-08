# from django.urls import path,include
# from rest_framework import routers
# from course import views as courseviews


# courserouter = routers.DefaultRouter()
# courserouter.register('',courseviews.ClassViewSet)


# sectionrouter = routers.DefaultRouter()
# sectionrouter.register('student',courseviews.SectionStudentViewSet)
# sectionrouter.register('teacher',courseviews.TeacherSectionViewSet)
# sectionrouter.register('courseviews',courseviews.SectionRoutineViewSet)
# sectionrouter.register('',courseviews.SectionViewSet)

# urlpatterns=[
# 	path('class',include(courserouter.urls)),
# 	path('section',include(sectionrouter.urls))
# ]
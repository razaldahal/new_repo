from rest_framework.routers import DefaultRouter
from django.urls import path,include

from academics import views

router=DefaultRouter()

router.register('timetable',views.TimetableViewSet)
#router.register('config',views.AcademicConfigViewSet)

urlpatterns =[
	path('',include(router.urls)),
]





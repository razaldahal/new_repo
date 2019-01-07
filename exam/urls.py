from rest_framework.routers import DefaultRouter
from exam import views
from django.urls import include,path

router=DefaultRouter()

router.register('term',views.TermViewset)
router.register('schedule',views.ScheduleViewset)
router.register('addmarks',views.AddMarksViewSet)
router.register('studentmarks',views.StudentmarksViewSet)




urlpatterns = [
	path('',include(router.urls))
]
from rest_framework.routers import DefaultRouter
from event import views
from django.urls import include,path

router=DefaultRouter()

router.register('event',views.EventViewSet)
router.register('type',views.EventTypeViewSet)





urlpatterns = [
	path('',include(router.urls))
]
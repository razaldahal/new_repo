from rest_framework.routers import DefaultRouter
from event import views
from django.urls import include,path

router=DefaultRouter()

router.register('',views.EventViewSet)





urlpatterns = [
	path('',include(router.urls))
]
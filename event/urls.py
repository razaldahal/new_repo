from django.urls import path,include

from rest_framework import routers

from event import views

router = routers.DefaultRouter()
router.register('type',views.EventTypeViewSet)
router.register('',views.EventViewSet)

urlpatterns = [
	path('',include(router.urls))
	]
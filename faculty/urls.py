from django.urls import path,include

from rest_framework import routers

from faculty import views

router = routers.DefaultRouter()
router.register('',views.FacultyViewSet)
urlpatterns = [
	path('',include(router.urls))
	]
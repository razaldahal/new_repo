from rest_framework.routers import DefaultRouter
from django.urls import path
from dashboard import views


router=DefaultRouter()


urlpatterns = [
	path('stat', views.StatsViewSet.as_view())
]    
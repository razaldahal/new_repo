from django.urls import path,include
from message import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register('',views.MessageViewSet)

urlpatterns = [
	path('',include(router.urls))

	]
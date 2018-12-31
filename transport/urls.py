from django.urls import path,include

from rest_framework import routers

from transport import views

router = routers.DefaultRouter()
router.register('vehicle',views.TransportViewSet)
router.register('busstaff',views.BusStaffViewset)
router.register('allocate',views.TransportAllocationViewSet)
router.register('route',views.RouteViewSet)
urlpatterns = [
	path('',include(router.urls))
	]
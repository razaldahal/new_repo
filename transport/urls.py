from django.urls import path,include

from rest_framework import routers

from transport import views

router = routers.DefaultRouter()
router.register('vehicle',views.VehicleViewSet)
router.register('staff',views.StaffViewSet)
router.register('allocate',views.VehicleAllocationViewSet)
urlpatterns = [
	path('',include(router.urls))
	]
from django.urls import path,include
from rest_framework import routers

from accountant import views

router = routers.DefaultRouter()
router.register(r'accountant',views.AccountantViewset)
router.register(r'payments',views.PaymentsViewSet)
router.register(r'ppr',views.Payment_posting_referenceViewsets)
router.register(r'fees',views.FeesdueViewSets)
urlpatterns = [
	path('',include(router.urls)),

	]
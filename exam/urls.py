from django.urls import path,include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'term',views.ExamTermViewset)
router.register(r'schedule',views.ExamScheduleViewset)
router.register(r'subject',views.SubjectViewSet)
router.register(r'marks-entry',views.MarksEntryViewSet)
router.register(r'view-result',views.ViewResultViewSet)
router.register(r'prepare_result',views.PrepareResultViewSet)


urlpatterns = [
    path('',include(router.urls))
]
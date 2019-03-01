
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="EduInfosys API",
      default_version='v1',
      description="API Specifications for EduInfosys Apps",
      #terms_of_service="",
      #contact=openapi.Contact(email="techackernp@gmail.com   "),
      #license=openapi.License(name=""),
   ),
   validators=[], ##['flex'], #, 'ssv'],
   public=True,
   permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/dashboard/',include('dashboard.urls')),
    path('api/academic/',include('academic.urls')),
    path('api/student/',include('student.urls')),
    path('api/faculty/',include('faculty.urls')),
    path('api/library/',include('library.urls')),
    path('api/transport/',include('transport.urls')),
    path('api/event/',include('event.urls')),
    path('api/exam/',include('exam.urls')),

    path('api/accounting/',include('accounting.urls')),
    path('api/store/',include('store.urls')),
     path('api/setting/',include('setting.urls')),
    # path('api/admission/',include('admission.urls')),
    # # path('api/class/',include('Class.urls')),
    # # path('api/section/',include('Section.urls')),
    # path('api/student/',include('student.urls')),
    # path('api/course/',include('course.urls')),
    # path('api/guardian/',include('guardian.urls')),
    # path('api/teacher/',include('teacher.urls')),
    # path('api/message/',include('message.urls')),
    
    # path('api/transport/',include('transport.urls')),
    # path('api/dashboard/',include('dashboard.urls')),
    # path('api/event/',include('event.urls')),
    # path('api/exam/',include('exam.urls')),

   # path('',include('api.urls')),

   url(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
   url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

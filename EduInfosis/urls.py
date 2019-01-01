"""EduInfosis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/library/',include('library.urls')),
    path('api/accountant/',include('accountant.urls')),
    path('api/admission/',include('admission.urls')),
    path('api/class/',include('Class.urls')),
    path('api/section/',include('Section.urls')),
    path('api/student/',include('student.urls')),
    path('api/course/',include('course.urls')),
    path('api/guardian/',include('guardian.urls')),
    path('api/teacher/',include('teacher.urls')),
    path('api/message/',include('message.urls')),
    path('api/academics/',include('academics.urls')),
    path('api/transport/',include('transport.urls')),
    path('api/dashboard/',include('dashboard.urls')),
    path('api/event',include('event.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

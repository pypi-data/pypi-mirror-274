"""openlxp_P1_notification_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()

app_name = 'openlxp_P1_notification'
urlpatterns = [
    path('get-email-request/<str:request_id>',
         views.EmailRequestView.as_view(),
         name='email-request'),
]

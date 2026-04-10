"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
#from rest_framework import routers

from apps.users.views import ConsumerLoginView, ConsumerLogoutView
from apps.consumers.views import ConsumerRegisterView, ConsumerProfileView
from apps.users.views import UserDetailView

from rest_framework import routers

#router = routers.DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/consumers/register/', ConsumerRegisterView.as_view()),
    path('api/consumers/login/', ConsumerLoginView.as_view()),
    path('api/consumers/logout/', ConsumerLogoutView.as_view()),
    path('api/consumers/profile/<int:user_id>/', ConsumerProfileView.as_view()),

    path('api/users/<int:user_id>/', UserDetailView.as_view()),

    path('api/', include('apps.catalog.urls')),

]

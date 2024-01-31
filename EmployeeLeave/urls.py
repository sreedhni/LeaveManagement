"""
URL configuration for EmployeeLeave project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from Leave import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.index,name="index"),
    path("ad/register/",views.ad_register,name="ad-register"),
    path("ad/login/",views.ad_login,name="ad-login"),
    path("ad/leave/all",views.AdLeaveListView.as_view(),name="admin"),
    path('ad/leave/<int:pk>/edit/',views.ALeaveUpdateView.as_view(),name="aleave-edit"),


    path("usr/register/",views.usr_register,name="usr-register"),
    path("usr/login/",views.usr_login,name="usr-login"),
    path('usr/leave/add/',views.EmployeeLeaveCreateView.as_view(),name="leave-add"),
    path('usr/leave/<int:pk>/edit/',views.EmployeeLeaveUpdateView.as_view(),name="leave-edit"),
    path('usr/leave/<int:pk>/delete/',views.remove_leaveview,name="leave-remove"),
    path("usr/<int:pk>/",views.LeaveDetailView.as_view(),name="leave-detail"),
   
    path("usr/leave/all",views.ULeaveListView.as_view(),name="user"),

    path('logout/',views.sign_outview,name="log-out")



]

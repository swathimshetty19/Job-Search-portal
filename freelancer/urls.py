"""freelancer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from freelancerapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('invalid/',views.invalidview,name='invalidview'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('skills/<str:pk>/', views.skills, name='skills'),
    path('skills/<str:pk>/search/',views.search_titles),
    path('skills/get/<str:pk>/<str:skill>/',views.add_skill,name='add_skill'),
    path('post_project/<str:pk>/',views.post_project,name='post_project'),
    path('otherdetails/<str:pk>/',views.other_details,name='other_details'),
    path('myprojects/<str:pk>/',views.myprojects,name='myprojects'),
    path('myproj/<str:pk>/<str:proj>/',views.myproj,name='myproj'),
    path('hire/<str:pk>/<str:proj>/<str:name>/',views.hire,name='hire'),
    path('proj_applied/<str:pk>/<str:proj>/',views.proj_applied,name='proj_applied'),
    path('browse/<str:user>',views.browse,name='browse'),
    path('browse_pro_desc/<str:pid>/<str:pk>',views.browse_pro_desc,name='browse_pro_desc')
]

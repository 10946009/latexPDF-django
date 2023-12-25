"""
URL configuration for getZerojudge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from outfile.views  import create, get_zerojudge
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', create.create),
    path('create/<int:cid>', create.create),
    path('getZerojudge/<int:cid>', get_zerojudge.get_zerojudge)
]

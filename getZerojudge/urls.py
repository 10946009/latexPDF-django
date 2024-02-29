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
from outfile.views import create, get_zerojudge, PathManager, index,problem_crud,pdf,generator

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index.index, name="index"),
    path("delete/", problem_crud.delete_problem, name="delete_problem"),
    path("create/problem", problem_crud.create, name="create_problem"),
    path("create/<int:cid>", create.create, name="create"),
    path("create/<int:cid>/downloadZIP", create.download_zip),
    path("getZerojudge/<int:cid>", get_zerojudge.get_zerojudge),

    path("pdf/get/<int:cid>", pdf.get, name="get_pdf"),
    path('get/generator/', generator.generator, name='generator'),

]

"""
URL configuration for myormproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from ninja import NinjaAPI
from app.api.api import router
from app.api.api_scrap import router as router_scrap
from app.api.api_save_ondata import router as router_save_ondata

api = NinjaAPI()

api.add_router("/evento", router, tags=["Operações mysql"])
api.add_router("/scrap", router_scrap , tags=["Operações de scrap"])
api.add_router("/save", router_save_ondata, tags=["Operações de salvar dados através do Scrap"])

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]

"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from core.API.utils.auth import AuthBearer
from django.contrib.admin.views.decorators import staff_member_required
from core.API.routes.auth import router as auth_router
from core.API.routes.review import router as books_router


api = NinjaAPI(
    title="Book Review",
    description="Book Review API",
    version="v1",
    auth=AuthBearer(),
    docs_decorator=staff_member_required,
)
api.add_router("/auth/", auth_router, tags=["Auth"])
api.add_router("/books/", books_router, tags=["Books"])

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]

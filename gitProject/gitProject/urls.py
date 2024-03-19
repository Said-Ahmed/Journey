"""
URL configuration for gitProject project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from git import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_place/', views.CreatePlaceView.as_view()),
    path('categories/', views.GetCategoryView.as_view()),
    path('map_places/', views.GetPlaceMapView.as_view()),
    path('search_places/', views.SearchPlaces.as_view()),
    path('place_detail/<int:pk>/', views.PlaceDetail.as_view(), name='place_detail'),
    path('places_by_ids/', views.GetPlacesByIds.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

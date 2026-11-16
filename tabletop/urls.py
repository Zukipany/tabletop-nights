from django.urls import include, path

urlpatterns = [
    path('', include('common.urls')),
    path('games/', include('catalog.urls')),
]

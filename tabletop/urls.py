from django.urls import include, path

urlpatterns = [
    path('', include('common.urls')),
    path('games/', include('catalog.urls')),
    path('players/', include('players.urls')),
    path('nights/', include('nights.urls')),
]

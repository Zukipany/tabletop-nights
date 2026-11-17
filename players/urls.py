from django.urls import include, path

from players import views

urlpatterns = [
    path('', views.PlayerListView.as_view(), name='player-list'),
    path('add/', views.PlayerCreateView.as_view(), name='player-create'),
    path('<int:pk>/', include([
        path('', views.PlayerDetailView.as_view(), name='player-detail'),
        path('edit/', views.PlayerUpdateView.as_view(), name='player-edit'),
        path('delete/', views.PlayerDeleteView.as_view(), name='player-delete'),
    ])),
]

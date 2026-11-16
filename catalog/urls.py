from django.urls import include, path

from catalog import views

urlpatterns = [
    path('', views.GameListView.as_view(), name='game-list'),
    path('add/', views.GameCreateView.as_view(), name='game-create'),
    path('<int:pk>/', include([
        path('', views.GameDetailView.as_view(), name='game-detail'),
        path('edit/', views.GameUpdateView.as_view(), name='game-edit'),
        path('delete/', views.GameDeleteView.as_view(), name='game-delete'),
    ])),
]

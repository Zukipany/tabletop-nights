from django.urls import include, path

from nights import views

urlpatterns = [
    path('', views.NightListView.as_view(), name='night-list'),
    path('add/', views.NightCreateView.as_view(), name='night-create'),
    path('<int:pk>/', include([
        path('', views.NightDetailView.as_view(), name='night-detail'),
        path('edit/', views.NightUpdateView.as_view(), name='night-edit'),
        path('delete/', views.NightDeleteView.as_view(), name='night-delete'),
    ])),
]

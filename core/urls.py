from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('advisory/', views.get_advisory, name='get_advisory'),
    path('result/<int:pk>/', views.result_view, name='result'),
    path('history/', views.history, name='history'),
    path('api/predict/', views.api_predict, name='api_predict'),
]

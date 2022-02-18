from django.urls import path

from src.oauth.endpoint import views

urlpatterns = [
    path('profile/<int:pk>/', views.ProfileView.as_view()),
    path('profile/<int:pk>/update/', views.UserView.as_view()),
    path('social/', views.SocialLinkView.as_view(
        {'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}
    ))

]
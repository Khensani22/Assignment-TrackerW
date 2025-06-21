from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from .views import CustomLoginView
from .views import custom_logout_view


urlpatterns = [
    # Views that require login protection
    path('assignments_list/', views.assignments_list, name='assignments_list'),
    path('add_assignment/', views.add_assignment, name='add_assignment'),
    path('add_assignment/<int:assignment_id>/', views.add_assignment, name='update_assignment'),
    path('delete_assignment/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    path('approaching_duedates/', views.approaching_duedates, name='approaching_duedates'),

    # Authentication Views
    path('register/', views.register, name='register'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
   path('accounts/logout/', views.custom_logout_view, name='logout'),


    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # Public pages
    path('homepage/', views.homepage, name='home'),
    path('about/', views.about, name='about'),
]


 


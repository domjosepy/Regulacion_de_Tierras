from django.urls import path
from sistema import views

app_name = 'sistema'

# URL configuration for the 'sistema' app
urlpatterns = [
    # Login, Sign Up, Home, Password Change, Edit Profile, and Test Toast URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('password_change/', views.CustomPasswordChangeView.as_view(),
         name='password_change_form'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('test_toast/', views.test_toast, name='test_toast'),
]

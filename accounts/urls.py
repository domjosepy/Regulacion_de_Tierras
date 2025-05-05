from django.urls import path
from .views import SignUpView, edit_profile, HomeView, test_toast

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("edit_profile/", edit_profile, name="edit_profile"),
    path('', HomeView.as_view(), name='home'),
    path('test-toast/', test_toast, name='test_toast'),

]

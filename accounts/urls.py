from django.urls import path

from .views import sign_up, login_view, logout_view, user_profile_edit

app_name = 'accounts'

urlpatterns = [
    path('signup/', sign_up, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile-edit/', user_profile_edit, name='user_profile_edit'),
]

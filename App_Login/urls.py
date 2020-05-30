from django.urls import path
from App_Login import views

app_name = 'App_Login'

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile, name='profile'),
    path('user/<user_is>/', views.searching_user, name='searching_user'),
    path('follow/<user_is>', views.follow, name='follow'),
    path('unfollow/<user_is>', views.unfollow, name='unfollow'),
]

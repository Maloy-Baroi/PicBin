from django.urls import path
from App_Post import views

app_name = 'App_Post'

urlpatterns = [
    path('', views.home, name='home'),
    path('loved/<pk>/', views.loved, name='loved'),
    path('no-loved/<pk>/', views.no_loved, name='no_loved'),
    path('comment/<pk>/', views.comment_post, name='comment'),
    path('details-my-picture/<pk>/', views.PostDetails.as_view(), name='details_my_picture'),
    path('delete-post/<pk>/', views.delete_mypost, name='delete_post'),
    path('update-post/<pk>/', views.UpdatePost.as_view(), name='update_post'),
]


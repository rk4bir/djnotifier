from django.urls import path
from .views import anonymous_users_view, authenticated_user_view, notify

app_name = 'example'

urlpatterns = [
    path("", anonymous_users_view, name='noauth'),
    path("auth/", authenticated_user_view, name='auth'),
    path("notify/", notify, name='notify')
]

from django.urls import path

from . import views

app_name = 'user'

"""name is to match with the name we are calling this api in test."""

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]

from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('<int:user_id>', views.user, name='user'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_out/<int:user_id>', views.sign_out, name='sign_out'),
]
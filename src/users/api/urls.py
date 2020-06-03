from django.urls import path
from .views import SignIn, SignUp

urlpatterns = [
    path('register/', SignUp.as_view()),
    path('login/', SignIn.as_view())
]
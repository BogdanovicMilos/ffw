from django.contrib import admin
from django.urls import path
from .views import AddView, CalculateView, ResetView, HistoryView, HistoryList

urlpatterns = [
    path('add/', AddView.as_view()),
    path('calculate/', CalculateView.as_view()),
    path('calculate/<slug:all>/', CalculateView.as_view()),
    path('reset/', ResetView.as_view()),
    path('history/', HistoryList.as_view()),
    path('history/<int:pk>/', HistoryView.as_view()),
]
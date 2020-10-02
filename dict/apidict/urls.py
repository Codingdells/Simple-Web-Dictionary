from .import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('results/', views.results, name="results"),
]

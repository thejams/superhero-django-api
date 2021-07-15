from django.urls import path
from superhero import views

urlpatterns = [
    path('superheroe/', views.SuperheroeApi.as_view()),  
    path('superheroe/<str:id>', views.SuperheroeApi.as_view()),     
]

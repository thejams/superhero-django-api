from django.urls import path
from django.conf.urls import url
from superhero import views

urlpatterns = [
    path('superhero/', views.SuperheroeApi.as_view(), name='get_post_superheroes'),  
    path('superhero/<str:id>', views.SuperheroeApi.as_view(), name='get_delete_put_single_superhero'),
    path('health/', views.HealthCheck.as_view(), name='health_check')
]

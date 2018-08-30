
from django.urls import path,include
from botskill import views

app_name = "botskill"

urlpatterns = [
    path('demo/', views.index, name='index'),
]

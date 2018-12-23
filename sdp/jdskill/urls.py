
from django.urls import path,include
from . import views

app_name = "jdskill"

urlpatterns = [
    path('demo/', views.index, name='index'),
]

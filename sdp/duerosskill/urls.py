from django.urls import path
from duerosskill import views

app_name = "duerosskill"

urlpatterns = [
    path('demo/', views.index, name='index'),
]

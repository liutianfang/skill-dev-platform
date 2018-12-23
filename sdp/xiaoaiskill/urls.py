
from django.urls import path,include
from  xiaoaiskill  import views

app_name = "xiaoaiskill"

urlpatterns = [
    path('demo/', views.index, name='index'),
]

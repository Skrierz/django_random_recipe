from django.urls import path
from . import views


app_name = 'recipe'
urlpatterns = [
    path('<int:pk>/', views.index, name='dish')
]

from django.urls import path

from .views import create_categories, get_categories

urlpatterns = [
    path('', create_categories),
    path('<int:pk>', get_categories),
]

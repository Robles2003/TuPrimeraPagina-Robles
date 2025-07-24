from django.urls import path
from .views import PruebaUSUARIOView

urlpatterns = [
    path('pruebaUSUARIO/', PruebaUSUARIOView.as_view(), name='pruebaUSUARIO'),
]

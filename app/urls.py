from django.urls import path
from app.views import PizzaTypesAPI, PizzaSizeAPI, PizzaToppingAPI, PizzaAPI

urlpatterns = [
    path("pizza/types/", PizzaTypesAPI.as_view()),
    path("pizza/size/", PizzaSizeAPI.as_view()),
    path("pizza/topping/", PizzaToppingAPI.as_view()),
    path("pizza/<int:pk>/", PizzaAPI.as_view()),
    path("pizza/", PizzaAPI.as_view())
]
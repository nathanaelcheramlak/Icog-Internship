from django.urls import path
from . import views

urlpatterns = [
    path("populate/", views.populate_db, name="populate_db"),
    path("predict/", views.predict_fare, name="predict_fare"),
]

from django.urls import path
from . import views, auth
urlpatterns = [
    path('', auth.login),
    path('register', auth.registro),
    path('login', auth.login),
    path('logout', auth.logout),
    path('travels',views.index),
    path('add',views.add),
    path('add_trip',views.add_trip),
    path('<trip_id>/cancel',views.cancel_trip),
    path('<trip_id>/delete',views.delete_trip),
    path('<trip_id>/join',views.join_trip),
    path('<trip_id>/view',views.view_trip)
]

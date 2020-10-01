from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('process/', views.process_payment, name='process'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
]

from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:catagory_slug>/', views.product_list,
         name='product_list_by_catagory'),
    path('<int:id>/<slug:slug>/', views.product_details, name='product_details')
]

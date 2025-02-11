"""
URL configuration for pythonProjectPolina project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('about/', views.about, name='about'),
    path('', views.index, name='index'),
    path('contacts/', views.contacts, name='contacts'),
    path('shtraf/', views.shtraf, name='shtraf'),
    path('sales/', views.sales, name='sales'),
    path('news/', views.news, name='news'),
    path('feedback/', views.feedback, name='feedback'),
    path('slovar/', views.faq, name='slovar'),
    path('vac/', views.vac, name='vac'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('slovar/', views.faq, name='slovar'),
    path('add_feedback/', views.add_feedback, name='add_feedback'),
    path('custom/', views.customer, name='custom'),
    path('sell/', views.seller, name='sell'),
                  path('car/', views.car, name='car'),
                  path('add_car/', views.add_car, name='add_car'),
                  path('add_to_bron/<int:car_id>', views.add_to_bron, name='add_to_bron'),
                  path('orders/', views.order_list, name='order_list'),
                  path('add_mark/', views.add_mark, name='add_mark'),
                  path('foradmin/', views.foradmin, name='foradmin'),
                  path('filter/', views.filter_cars, name='filter'),
                  path('search/', views.search_view, name='search'),
                  path('order_cost/', views.order_cost, name='order_costs'),
                  
path('update/<int:item_id>/', views.update_order_item, name='update_order_item'),
    path('delete/<int:item_id>/', views.delete_order_item, name='delete_order_item'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
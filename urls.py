from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import address_list, add_address, edit_address, delete_address, custom_logout, seed_medicines


urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),

    # Cart & Order
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('confirm-order/', views.confirm_order, name='confirm_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Prescription upload
    path('upload-prescription/', views.upload_prescription, name='upload_prescription'),
    path('upload-success/', views.upload_success, name='prescription_success'),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='account_login'),
    path('set-pincode/', views.set_pincode, name='set_pincode'),
    path('search/', views.search_view, name='search'),
    path('medicine/<int:pk>/', views.medicine_detail, name='medicine_detail'),
    path('addresses/', address_list, name='addresses_list'),
    path('addresses/add/', add_address, name='add_address'),
    path('addresses/edit/<int:pk>/', edit_address, name='edit_address'),
    path('addresses/delete/<int:pk>/', delete_address, name='delete_address'),
    path('logout/', custom_logout, name='logout'),
    path('seed-medicines/', seed_medicines, name='seed_medicines'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
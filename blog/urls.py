from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),


    # Static Pages
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/oil/', views.oil_trading, name='service_oil'),
    path('services/gas/', views.gas_management, name='service_gas'),
    path('services/consulting/', views.consulting, name='service_consulting'),
    path('contact/', views.contact, name='contact'),

    # Equipment CRUD
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/add/', views.equipment_add, name='equipment_add'),
    path('equipment/edit/<int:pk>/', views.equipment_edit, name='equipment_edit'),
    path('equipment/delete/<int:pk>/', views.equipment_delete, name='equipment_delete'),

    # Suppliers CRUD
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.supplier_add, name='supplier_add'),
    path('suppliers/edit/<int:pk>/', views.supplier_edit, name='supplier_edit'),
    path('suppliers/delete/<int:pk>/', views.supplier_delete, name='supplier_delete'),

    # Stock CRUD
    path('stock/', views.stock_list, name='stock_list'),
    path('stock/add/', views.stock_add, name='stock_add'),
    path('stock/edit/<int:pk>/', views.stock_edit, name='stock_edit'),
    path('stock/delete/<int:pk>/', views.stock_delete, name='stock_delete'),
    path('stock/low/', views.low_stock, name='low_stock'),
    path('stock/data/', views.stock_data, name='stock_data'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Vehicle Records
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.vehicle_add, name='vehicle_add'),
    path('vehicles/edit/<int:pk>/', views.vehicle_edit, name='vehicle_edit'),
    path('vehicles/delete/<int:pk>/', views.vehicle_delete, name='vehicle_delete'),
    path('vehicles/exit/<int:pk>/', views.vehicle_exit, name='vehicle_exit'),
    path('vehicles/pdf/<int:pk>/', views.vehicle_pdf, name='vehicle_pdf'),
    path('vehicles/report/pdf/', views.vehicle_report_pdf, name='vehicle_report_pdf'),

    # Authentication (Custom)
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('register/', views.register, name='register'),

    # PDF Testing
    path('test-pdf/', views.test_pdf, name='test_pdf'),
]
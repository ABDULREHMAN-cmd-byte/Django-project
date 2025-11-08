from django.db import models
from django.utils import timezone

# Contact Form
class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


# Project Info
class Project(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    manager = models.CharField(max_length=100)
    start_date = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Supplier Details (Petroleum/Gas Industry)
class Supplier(models.Model):
    COMPANY_TYPES = [
        ("Refinery", "Refinery"),
        ("Distributor", "Distributor"),
        ("Gas Supplier", "Gas Supplier"),
        ("Transporter", "Transporter"),
    ]
    name = models.CharField(max_length=150)
    company_type = models.CharField(max_length=50, choices=COMPANY_TYPES, default="Refinery")
    contact_person = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.company_type})"


# Equipment (Tanks, Pumps, etc.)
class Equipment(models.Model):
    EQUIPMENT_TYPES = [
        ("Pump", "Pump"),
        ("Compressor", "Compressor"),
        ("Storage Tank", "Storage Tank"),
        ("Pipeline", "Pipeline"),
    ]
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=120, choices=EQUIPMENT_TYPES)
    condition = models.CharField(max_length=50, choices=[
        ('Good', 'Good'),
        ('Needs Repair', 'Needs Repair'),
        ('Out of Order', 'Out of Order'),
    ], default='Good')
    location = models.CharField(max_length=150, blank=True)
    storage_capacity = models.FloatField(default=0, help_text="Capacity in barrels or cubic meters")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Inspection Records
class Inspection(models.Model):
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE)
    inspector = models.CharField(max_length=100)
    remarks = models.TextField(blank=True)
    passed = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.equipment.name} ({self.date})"


# Stock Management (Fuel, Gas, etc.)
class StockItem(models.Model):
    FUEL_TYPES = [
        ("Petrol", "Petrol"),
        ("Diesel", "Diesel"),
        ("Natural Gas", "Natural Gas"),
        ("LPG", "LPG"),
    ]
    name = models.CharField(max_length=150)
    fuel_type = models.CharField(max_length=50, choices=FUEL_TYPES, default="Petrol")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    min_level = models.PositiveIntegerField(default=100)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.fuel_type} ({self.quantity})"


# ✅ Vehicle Entry/Exit Records (Updated with driver_phone)
class VehicleRecord(models.Model):
    VEHICLE_TYPES = [
        ('Tanker', 'Tanker'),
        ('Truck', 'Truck'),
        ('Service', 'Service Vehicle'),
        ('Other', 'Other'),
    ]
    vehicle_number = models.CharField(max_length=50)
    driver_name = models.CharField(max_length=100)
    driver_phone = models.CharField(max_length=15, blank=True, null=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES, default='Tanker')
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)
    product_type = models.CharField(max_length=100, help_text="e.g. Petrol, Diesel, Gas")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Litres or KG")
    remarks = models.TextField(blank=True)
    checked_by = models.CharField(max_length=100, blank=True)
    print_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.vehicle_number} - {self.product_type}"

    def duration(self):
        if self.exit_time:
            return self.exit_time - self.entry_time
        return None


# ✅ Properly defined Vehicle model
class Vehicle(models.Model):
    vehicle_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=50)
    driver_name = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=50, choices=[
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('CNG', 'CNG'),
        ('LPG', 'LPG'),
    ])
    capacity = models.CharField(max_length=50, help_text="Total Tank Capacity (e.g., 5000 liters)")
    last_service_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('Active', 'Active'),
        ('Under Maintenance', 'Under Maintenance'),
        ('Inactive', 'Inactive'),
    ])
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle_name} - {self.registration_number}"
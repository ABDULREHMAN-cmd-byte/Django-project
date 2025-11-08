from django.contrib import admin
from django.shortcuts import render
from .models import Contact, Project, Supplier, Equipment, StockItem, Inspection, VehicleRecord
from django.contrib.auth.decorators import login_required

# ----------------------------
# CONTACT ADMIN
# ----------------------------
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'date')
    search_fields = ('name', 'email', 'subject')


# # ----------------------------
# # PROJECT ADMIN
# # ----------------------------
# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'description')
#     search_fields = ('title',)


# ----------------------------
# SUPPLIER ADMIN
# ----------------------------
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact_person', 'phone', 'email', 'date_added')
    search_fields = ('name', 'contact_person', 'phone')


# ----------------------------
# EQUIPMENT ADMIN
# ----------------------------
@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'condition', 'location', 'date_added')
    search_fields = ('name', 'type', 'location')
    list_filter = ('condition', 'type')


# ----------------------------
# STOCK ITEM ADMIN
# ----------------------------
@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'supplier', 'quantity', 'min_level', 'last_updated')
    search_fields = ('name',)
    list_filter = ('supplier',)


# # ----------------------------
# # INSPECTION ADMIN
# # ----------------------------
# @admin.register(Inspection)
# class InspectionAdmin(admin.ModelAdmin):
#     list_display = ('id', 'equipment', 'inspector_name', 'inspection_date', 'status')
#     search_fields = ('equipment__name', 'inspector_name')
#     list_filter = ('status',)

@admin.register(VehicleRecord)
class VehicleRecordAdmin(admin.ModelAdmin):
    list_display = ('vehicle_number', 'driver_name', 'driver_phone', 'supplier', 'product_type', 'quantity', 'entry_time', 'exit_time')
    search_fields = ('vehicle_number', 'driver_name', 'supplier__name', 'product_type')
    list_filter = ('vehicle_type', 'product_type', 'supplier')    
    
@login_required
def dashboard(request):
    # only logged in users can access
    return render(request, 'dashboard.html')
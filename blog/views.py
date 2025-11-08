from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import F, Sum 
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from .models import Equipment, Supplier, StockItem, VehicleRecord, Vehicle
from .forms import EquipmentForm, RegisterForm, SupplierForm, StockItemForm, VehicleRecordForm,UserLoginForm

# ------------------ Static Pages ------------------

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

def oil_trading(request):
    return render(request, 'oil_trading.html')

def gas_management(request):
    return render(request, 'gas_management.html')

def consulting(request):
    return render(request, 'consulting.html')

# ------------------ Equipment CRUD ------------------

def equipment_list(request):
    equipments = Equipment.objects.all()
    return render(request, 'equipment/list.html', {'equipments': equipments})

def equipment_add(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment added successfully!')
            return redirect('equipment_list')
    else:
        form = EquipmentForm()
    return render(request, 'equipment/add.html', {'form': form})

def equipment_edit(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment updated successfully!')
            return redirect('equipment_list')
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'equipment/edit.html', {'form': form, 'equipment': equipment})

def equipment_delete(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        equipment.delete()
        messages.success(request, 'Equipment deleted successfully!')
        return redirect('equipment_list')
    return render(request, 'equipment/delete.html', {'equipment': equipment})

# ------------------ Supplier CRUD ------------------

def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'suppliers/list.html', {'suppliers': suppliers})

def supplier_add(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier added successfully!')
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'suppliers/add.html', {'form': form})

def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier updated successfully!')
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'suppliers/edit.html', {'form': form})

def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    messages.success(request, 'Supplier deleted successfully!')
    return redirect('supplier_list')

# ------------------ Stock CRUD ------------------

def stock_list(request):
    stocks = StockItem.objects.all()
    return render(request, 'stock/list.html', {'stocks': stocks})

def stock_add(request):
    if request.method == 'POST':
        form = StockItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock item added successfully!')
            return redirect('stock_list')
    else:
        form = StockItemForm()
    return render(request, 'stock/add.html', {'form': form})

def stock_edit(request, pk):
    stock_item = get_object_or_404(StockItem, pk=pk)
    if request.method == 'POST':
        form = StockItemForm(request.POST, instance=stock_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock item updated successfully!')
            return redirect('stock_list')
    else:
        form = StockItemForm(instance=stock_item)
    return render(request, 'stock/edit.html', {'form': form})

def stock_delete(request, pk):
    stock_item = get_object_or_404(StockItem, pk=pk)
    stock_item.delete()
    messages.success(request, 'Stock item deleted successfully!')
    return redirect('stock_list')

def stock_data(request):
    data = list(StockItem.objects.values('name', 'quantity'))
    return JsonResponse(data, safe=False)

# ------------------ Dashboard ------------------

def dashboard(request):
    total_equipment = Equipment.objects.count()
    total_suppliers = Supplier.objects.count()
    total_stock_items = StockItem.objects.count()
    total_quantity = StockItem.objects.aggregate(total=Sum('quantity'))['total'] or 0
    low_stock_count = StockItem.objects.filter(quantity__lte=F('min_level')).count()

    # Chart data (Top 10)
    top_items = StockItem.objects.order_by('-quantity')[:10]
    chart_labels = [item.name for item in top_items]
    chart_data = [item.quantity for item in top_items]

    context = {
        'total_equipment': total_equipment,
        'total_suppliers': total_suppliers,
        'total_stock_items': total_stock_items,
        'total_quantity': total_quantity,
        'low_stock_count': low_stock_count,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }

    return render(request, 'dashboard.html', context)

# ------------------ Low Stock JSON ------------------

def low_stock(request):
    low_items_qs = StockItem.objects.filter(quantity__lte=F('min_level'))
    low_items = list(low_items_qs.values('id', 'name', 'quantity', 'min_level'))
    low_stock_count = low_items_qs.count()

    if request.GET.get('format') == 'json':
        return JsonResponse({'low_stock_count': low_stock_count, 'low_items': low_items})
    return render(request, 'stock/low_stock.html', {'low_items': low_items_qs})

# ------------------ Vehicle Record Management ------------------

def vehicle_list(request):
    vehicles = VehicleRecord.objects.all().order_by('-entry_time')
    return render(request, 'vehicles/list.html', {'vehicles': vehicles})

def vehicle_add(request):
    if request.method == 'POST':
        form = VehicleRecordForm(request.POST)
        if form.is_valid():
            v = form.save()
            messages.success(request, 'Vehicle record added successfully.')
            return redirect('vehicle_list')
    else:
        form = VehicleRecordForm()
    return render(request, 'vehicles/add.html', {'form': form})

  # Mark exit time
def vehicle_exit(request, pk):
    vehicle = get_object_or_404(VehicleRecord, pk=pk)
    vehicle.exit_time = timezone.now()
    vehicle.save()
    messages.success(request, 'Vehicle exit time recorded successfully.')
    return redirect('vehicle_list')

def vehicle_edit(request, pk):
    vehicle = get_object_or_404(VehicleRecord, pk=pk)
    if request.method == 'POST':
        form = VehicleRecordForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')  # apne list page ka name idhar likho
    else:
        form = VehicleRecordForm(instance=vehicle)
    return render(request, 'blog/vehicle_edit.html', {'form': form, 'vehicle': vehicle})

def vehicle_delete(request, pk):
    vehicle = get_object_or_404(VehicleRecord, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle record deleted successfully!')
        return redirect('vehicle_list')  # apne list view ka name rakho
    return render(request, 'vehicles/vehicle_delete.html', {'vehicle': vehicle})

def vehicle_record_list(request):
    records = VehicleRecord.objects.all()
    return render(request, 'vehicle_record_list.html', {'records': records}) 

# ✅ Add new vehicle record from frontend
def add_vehicle_record(request):
    if request.method == 'POST':
        form = VehicleRecordForm(request.POST)
        if form.is_valid():
            form.save()
            print("✅ Record added successfully")
            return redirect('vehicle_record_list')
        else:
                print("❌ Form errors:", form.errors)
    else:
        form = VehicleRecordForm()
    return render(request, 'add_vehicle_record.html', {'form': form})  

# 🚗 Vehicle Record List (Frontend)
def vehicle_list(request):
    vehicles = VehicleRecord.objects.all().order_by('-entry_time')
    return render(request, 'vehicles/list.html', {'vehicles': vehicles})

# 🚗 Add Vehicle Record
def vehicle_add(request):
    if request.method == 'POST':
        form = VehicleRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle added successfully!')
            return redirect('vehicle_list')
        else:
            messages.error(request, 'Form is invalid!')
    else:
        form = VehicleRecordForm()
    return render(request, 'vehicles/add.html', {'form': form})     

# ------------------ Vehicle Receipt PDF ------------------

def vehicle_pdf(request, pk):
    vehicle = get_object_or_404(VehicleRecord, pk=pk)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(300, 800, "Vehicle Receipt")

    p.setFont("Helvetica", 11)
    y = 760
    lines = [
        f"Vehicle No.: {vehicle.vehicle_number}",
        f"Vehicle Type: {vehicle.vehicle_type}",
        f"Driver: {vehicle.driver_name}    Phone: {vehicle.driver_phone or 'N/A'}",
        f"Supplier: {vehicle.supplier.name if vehicle.supplier else 'N/A'}",
        f"Product: {vehicle.product_type}",
        f"Quantity: {vehicle.quantity}",
        f"Entry Time: {vehicle.entry_time.strftime('%Y-%m-%d %H:%M')}",
        f"Exit Time: {vehicle.exit_time.strftime('%Y-%m-%d %H:%M') if vehicle.exit_time else '---'}",
        f"Checked By: {vehicle.checked_by or '---'}",
        f"Remarks: {vehicle.remarks or '---'}",
    ]
    for line in lines:
        p.drawString(60, y, line)
        y -= 18

    # footer
    p.setFont("Helvetica-Oblique", 9)
    p.drawString(60, 80, f"Generated: {timezone.now().strftime('%Y-%m-%d %H:%M')}")

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Vehicle_{vehicle.vehicle_number}.pdf"'
    return response


# ------------------ PDF Test View ------------------

def test_pdf(request):
    """Check if ReportLab is working fine"""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.drawString(100, 800, "✅ ReportLab working perfectly in Django!")
    pdf.drawString(100, 780, "This is a test PDF generated from your Django app.")
    pdf.save()
    
    pdf_value = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf_value, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="test.pdf"'
    return response

def generate_vehicle_pdf(request, record_id):
    # Record fetch karo
    record = VehicleRecord.objects.get(id=record_id)

    # Response ko PDF banane ke liye set karo
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="vehicle_{record.id}.pdf"'

    # ReportLab canvas banao
    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # PDF me likhna start karo
    pdf.setFont("Helvetica", 14)
    pdf.drawString(100, 800, "Vehicle Record Report")
    pdf.setFont("Helvetica", 12)

    y = 760
    pdf.drawString(100, y, f"Owner Name: {record.owner_name}")
    y -= 20
    pdf.drawString(100, y, f"Vehicle Number: {record.vehicle_number}")
    y -= 20
    pdf.drawString(100, y, f"Model: {record.model}")
    y -= 20
    pdf.drawString(100, y, f"Date Added: {record.date_added.strftime('%d-%m-%Y')}")

    # PDF save karo
    pdf.showPage()
    pdf.save()
    return response

def vehicle_report_pdf(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Vehicle Records Report")

    p.setFont("Helvetica", 12)
    y = 770
    vehicles = VehicleRecord.objects.all().order_by('-entry_time')

    if not vehicles.exists():
        p.drawString(100, y, "No vehicle records found.")
    else:
        for v in vehicles:
            p.drawString(100, y, f"Vehicle No: {v.vehicle_number} | Driver: {v.driver_name}")
            y -= 20
            p.drawString(120, y, f"Supplier: {v.supplier} | Product: {v.product_type} | Qty: {v.quantity}")
            y -= 20
            p.drawString(120, y, f"Entry: {v.entry_time.strftime('%Y-%m-%d %H:%M')}")
            if v.exit_time:
                p.drawString(120, y-20, f"Exit: {v.exit_time.strftime('%Y-%m-%d %H:%M')}")
                y -= 20
            y -= 30

            if y < 100:
                p.showPage()
                y = 770
                p.setFont("Helvetica", 12)

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="vehicle_report.pdf"'
    return response

# increment print counter
    vehicle.print_count = (vehicle.print_count or 0) + 1
    vehicle.save()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=Vehicle_{vehicle.vehicle_number}.pdf'
    return response

def custom_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(request, username=u, password=p)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully")
                return redirect('dashboard')   # اپنی مرضی کا route
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out")
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            messages.success(request, "Account created. You can login now.")
            return redirect('custom_login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
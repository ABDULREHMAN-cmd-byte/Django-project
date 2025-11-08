from django import forms
from .models import Equipment, Supplier, StockItem, VehicleRecord, Vehicle
from django.contrib.auth.models import User

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'type', 'condition', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class StockItemForm(forms.ModelForm):
    class Meta:
        model = StockItem
        fields = ['name', 'supplier', 'quantity', 'min_level']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'min_level': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

class VehicleRecordForm(forms.ModelForm):
    class Meta:
        model = VehicleRecord
        fields = ['vehicle_number', 'driver_name', 'driver_phone', 'supplier', 'vehicle_type', 'product_type', 'quantity', 'remarks', 'checked_by']
        widgets = {
            'vehicle_number': forms.TextInput(attrs={'class': 'form-control'}),
            'driver_name': forms.TextInput(attrs={'class': 'form-control'}),
            'driver_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
            'product_type': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'checked_by': forms.TextInput(attrs={'class': 'form-control'}),
        }

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
        
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('password2'):
            raise forms.ValidationError("Passwords do not match")
        return cleaned    
            
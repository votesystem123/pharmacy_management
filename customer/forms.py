from django import forms
from dashboard.models import Customer, suppiler, Medicine
from django.core.validators import RegexValidator

class AddCustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('name','phone_number', 'dr_name', 'dr_dept', 'dr_hospital')
        
        error_css_class = 'error_msg'
        required_css_class = "required"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'phar-cust-field'}),
            'phone_number': forms.TextInput(attrs={'class': 'phar-cust-field'}),
            'dr_name': forms.TextInput(attrs={'class': 'phar-cust-field'}),
            'dr_dept': forms.TextInput(attrs={'class': 'phar-cust-field'}),
            'dr_hospital': forms.TextInput(attrs={'class': 'phar-cust-field'}),
        }

class AddSupplierForm(forms.ModelForm):
    PAYMENT_CHOICES = (
        ("cash", "Cash"),
        ("upi", "Upi"),
        ("card", "Card"),
    )
    payment_type = forms.ChoiceField(choices=PAYMENT_CHOICES)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_type'].widget.attrs.update({'class': 'phar-cust-field'})

    class Meta:
        model = suppiler
        fields = ('suppiler_name', 'phone_number', 'company_name', 'payment_type')
        
        error_css_class = 'error_msg'
        required_css_class = "required"
        widgets = {
            'suppiler_name': forms.TextInput(attrs={'class': 'phar-cust-field select-supplier', 'id': 'supplier-select'}),
            'phone_number': forms.TextInput(attrs={'class': 'phar-cust-field', 'id': 'phone-number-input'}),
            'company_name': forms.TextInput(attrs={'class': 'phar-cust-field', 'id': 'company-name-input'}),
            'payment_type': forms.Select(attrs={'class': 'phar-cust-field', 'id': 'payment-type-input'}),
        }



class AddMedicineForm(forms.ModelForm):

    class Meta:
        model = Medicine
        fields = ('medicine_name','quantity', 'batch_id', 'exp_date','total_amount')
        exclude = ['suppiler_name', 'price']
        
        error_css_class = 'error_msg'
        required_css_class = "required"
        widgets = {
            'medicine_name': forms.TextInput(attrs={'class': 'phar-cust-field'}),
            'quantity': forms.TextInput(attrs={'class': 'phar-cust-field'}),
            'batch_id': forms.TextInput(attrs={'class': 'phar-cust-field'}),
            'exp_date': forms.TextInput(attrs={'class': 'phar-cust-field','autocomplete': 'off', 'type': 'date'}),
            'total_amount': forms.TextInput(attrs={'class': 'phar-cust-field'}),
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        quantity = instance.quantity
        total_amount = instance.total_amount
        if quantity is not None:
            instance.price = total_amount / quantity  # Assuming price is calculated based on quantity
        if commit:
            instance.save()
        return instance
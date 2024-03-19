from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
import json
from django.template.loader import render_to_string
from weasyprint import HTML

from customer.forms import AddCustomerForm,AddSupplierForm, AddMedicineForm

from dashboard.models import AiUser, suppiler, Medicine, Customer, Invoice, InvoiceItem

from django.utils import timezone
from dashboard.utils import download_template

@method_decorator(login_required(login_url='/'), name='dispatch')
class AddCutomerView(View):
    
    def get(self, request):
        form = AddCustomerForm()
        return render(request, 'customer/add_customer.html', {'form' : form})

    def post(self, request):
        try:
            form = AddCustomerForm(request.POST)
            if form.is_valid():
                user = form.save()
                return redirect('dashboard:dashboard')
            else:
                return render(request, 'customer/add_customer.html', {'form': form, 'error_message': 'invaild data'})
        except Exception as e:
            print("error--------------", str(e))
            return render(request, 'customer/add_customer.html', {'form': form, 'error_message': str(e)})
        
@method_decorator(login_required(login_url='/'), name='dispatch')
class CutomerListView(View):
    def get(self, request):
        customer_obj = Customer.objects.all().order_by('-date_created')
        return render(request, 'customer/view_customer.html',{'customer_obj':customer_obj})
    
@method_decorator(login_required(login_url='/'), name='dispatch')
class EditCustomerView(View):

    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = AddCustomerForm(instance=customer)
        return render(request, 'customer/edit_customer.html',{'form':form})
    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = AddCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer:customerlist')
        else:
            return render(request, 'customer/edit_customer.html', {'form': form, 'error_message': 'invaild data'})

@method_decorator(login_required(login_url='/'), name='dispatch')       
class ListsupplierView(View):
    def get(self, request):
        supplier_obj = suppiler.objects.all().order_by('-date_joined')
        return render(request, 'customer/view_supplier.html',{'supplier_obj':supplier_obj})

@method_decorator(login_required(login_url='/'), name='dispatch')
class ListMedicineView(View):
    def get(self, request):
        med_obj = Medicine.objects.all().order_by('-date_created')
        return render(request, 'customer/view_medicine.html',{'med_obj':med_obj})

@method_decorator(login_required(login_url='/'), name='dispatch')   
class AddSupplierView(View):
    def get(self, request):
        form = AddSupplierForm()
        return render(request, 'customer/add_supplier.html', {'form' : form})
    def post(self, request):
        try:
            form = AddSupplierForm(request.POST)
            if form.is_valid():
                supplier_instance = form.save()
                return redirect('customer:addmedicine')
            else:
                return render(request, 'customer/add_medicine.html', {'form': form, 'error_message': 'invaild data'})
        except Exception as e:
            print("error--------------", str(e))
            return render(request, 'customer/add_medicine.html', {'form': form, 'error_message': str(e)})

@method_decorator(login_required(login_url='/'), name='dispatch')
class PurchaseMedicineView(View):
    def get(self, request):
        form = AddSupplierForm()
        form2 = AddMedicineForm()
        supplier_obj = suppiler.objects.all().order_by('suppiler_name')
        if request.method == 'GET' and request.is_ajax():
            supplier_name = request.GET.get('supplier_name')
            try:
                supplier = suppiler.objects.get(suppiler_name=supplier_name)
                data = {
                    'phone_number': str(supplier.phone_number),
                    'company_name': supplier.company_name,
                    'payment_type': supplier.payment_type,
                }
                return JsonResponse(data)
            except suppiler.DoesNotExist:
                return JsonResponse({'error': 'Supplier not found'}, status=404)
        context ={
            'form' : form,
            'form2' : form2,
            'supplier_obj' : supplier_obj
        }
        return render(request, 'customer/add_medicine.html',context)
    def post(self, request):
        try:
            form = AddSupplierForm(request.POST)
            form2 = AddMedicineForm(request.POST)
            phone_number = form.data.get('phone_number')
            existing_supplier = suppiler.objects.filter(phone_number=phone_number).first()
            if existing_supplier:
                    supplier_instance = existing_supplier
                    print("Supplier with this phone number already exists")
            else:
                print("------------------else part-------------------")
                if form.is_valid():
                    supplier_instance = form.save()
                else:
                    supplier_obj = suppiler.objects.all()
                    return render(request, 'customer/add_medicine.html', {'form': form,'form2':form2,'supplier_obj':supplier_obj, 'error_message': 'invaild data'})
            if form2.is_valid(): 
                medicine_form = form2.save(commit=False)
                batch_id = medicine_form.batch_id 
                print("batch_id", batch_id)
                existing_medicine = Medicine.objects.filter(batch_id=batch_id).first()
                if existing_medicine:
                    # If medicine with same batch_id exists, update it
                    existing_medicine.medicine_name = medicine_form.medicine_name
                    existing_medicine.quantity += medicine_form.quantity
                    existing_medicine.exp_date = medicine_form.exp_date
                    existing_medicine.total_amount = medicine_form.total_amount
                    existing_medicine.price = medicine_form.price
                    existing_medicine.suppiler_name = supplier_instance
                    existing_medicine.date_created = timezone.now()
                    existing_medicine.save()
                else:
                    medicine_form.suppiler_name = supplier_instance
                    medicine_form.save()
                return redirect('customer:listmedicine')
            else:
                supplier_obj = suppiler.objects.all()
                return render(request, 'customer/add_medicine.html', {'form': form,'form2':form2,'supplier_obj':supplier_obj, 'error_message': 'invaild data'})
        except Exception as e:
            print("error--------------", str(e))
            return render(request, 'customer/add_medicine.html', {'form': form, 'form2':form2, 'error_message': str(e)})
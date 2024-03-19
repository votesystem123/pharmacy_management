from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
import json
from django.template.loader import render_to_string
from weasyprint import HTML

from dashboard.forms import SignUpForm, LoginForm

from dashboard.models import AiUser, suppiler, Medicine, Customer, Invoice, InvoiceItem

from django.utils import timezone
from dashboard.utils import download_template

# Create your views here.

class RegistrationView(View):
    
    def get(self, request):
        form = SignUpForm()
        return render(request, 'dashboard/register.html', {'form': form} )

    def post(self, request):
        try:
            form = SignUpForm(request.POST)
            print("form", form)
            if form.is_valid():
                user = form.save()
                return redirect('dashboard:login')
            return render(request, 'dashboard/register.html', {'form': form, 'error_message': 'invaild data'})
        except Exception as e:
            print("error--------------", str(e))
            return render(request, 'dashboard/register.html', {'form': form, 'error_message': str(e)})

class LoginView(View):
    
    def get(self, request):
        try:
            form = LoginForm()
            return render(request, 'dashboard/login.html',{'form': form} )
        except Exception as e:
            return render(request, 'dashboard/login.html', {'form': form, 'error_message': str(e)})
        
    def post(self, request):
        try:
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                user = authenticate(email=email, password=password)
                if user is not None :
                    login(request, user)
                    return redirect('dashboard:dashboard')
                else:
                    error_message = "Invalid username or password."
                    return render(request, 'dashboard/login.html', {'form': form, 'error_message':error_message})
            else:
                return render(request, 'dashboard/login.html', {'form': form, 'error_message': 'invaild data'})
        except Exception as e:
            return render(request, 'dashboard/login.html', {'form': form, 'error_message': str(e)})

class LogoutView(View):

    def get(self, request, format=None):
        logout(request)
        return redirect('dashboard:login')


@method_decorator(login_required(login_url='/'), name='dispatch')
class DashboardView(View):
    
    def get(self, request):
        user = request.user
        customer_obj = Customer.objects.all().count()
        invoice_obj = Invoice.objects.all().count()
        today_sales = Invoice.objects.filter(date_created__date = timezone.now().date()).count()
        today_purchase = Medicine.objects.filter(date_created__date = timezone.now().date()).count()
        expired_medicine = Medicine.objects.filter(exp_date__date__lte = timezone.now().date()).count()
        out_of_stock = Medicine.objects.filter(quantity__lte = 0).count()

        form_date = request.GET.get('date','')
        if not form_date:
            form_date = timezone.now().year

        total_sales_graph =  []
        for i in range(1,13):
            monthly_invoice = Invoice.objects.filter(Q(date_created__month = i) & Q(date_created__year = form_date)).count()
            total_sales_graph.append(monthly_invoice)
        
        total_purchase_graph = []
        for i in range(1,13):
            monthly_purchase = Medicine.objects.filter(Q(date_created__month = i) & Q(date_created__year = form_date)).count()
            total_purchase_graph.append(monthly_purchase)

        data_labels = ["JAN", "FEB", "MAR"]
        data_values = [10, 20, 30]
        context = {
            'user' : user,
            'customer_obj': customer_obj,
            'invoice_obj': invoice_obj,
            'today_sales': today_sales,
            'today_purchase': today_purchase,
            'expired_medicine': expired_medicine,
            'out_of_stock': out_of_stock,
            'total_sales_graph' : total_sales_graph,
            'total_purchase_graph' : total_purchase_graph,
        }
        return render(request, 'dashboard/home.html', context )
    
@method_decorator(login_required(login_url='/'), name='dispatch')
class InvoiceView(View):
    def get(self, request):
        user = request.user
        invoice_obj = Invoice.objects.all().order_by('-date_created')
        context= {
            'user' : user,
            'invoice_obj' : invoice_obj
        }
        return render(request, 'dashboard/invoice.html', context)

@method_decorator(login_required(login_url='/'), name='dispatch')
class CreateInvoiceView(View):
    def get(self, request):
        current_datetime = timezone.now()
        yesterday = current_datetime - timezone.timedelta(days=1)
        customer_obj = Customer.objects.all().order_by('name')
        med_obj = Medicine.objects.filter(exp_date__gt = yesterday, quantity__gt= 0)
        if request.method == 'GET' and request.is_ajax():
            search_value = request.GET.get('search', '')
            param = request.GET.get('param', '')
            if param == 'customer':
                customer_obj = Customer.objects.get(name__icontains = search_value)
                data = {
                    'contact_id': customer_obj.id,
                    'contact_name': str(customer_obj.name),
                    'contact_number': str(customer_obj.phone_number),
                    'contact_date': timezone.now().date(),
                }
            else:
                med_obj = Medicine.objects.get(medicine_name__icontains = search_value)
                data ={
                    'medicine_id': med_obj.id,
                    'medicine_name': str(med_obj.medicine_name),
                    'batch_number': str(med_obj.batch_id),
                    'amount': str(med_obj.price),
                    'exp_date': med_obj.exp_date.date(),
                    'quantity': str(med_obj.quantity),
                    'price': str(med_obj.price),
                }
            return JsonResponse(data)

        context= {
            'customer_obj' : customer_obj,
            'med_obj' : med_obj,
        }
        return render(request, 'dashboard/create_invoice.html', context)
    
    def post(self, request):
        try:
            contact_id = request.POST.get('contactid','None')
            Payment_type = request.POST.get('Paymenttype','None')
            total_amount = Payment_type = request.POST.get('totalamount','None')
            print("Payment_type",Payment_type)
            if contact_id != 'hidden_value':
                medicines_json = request.POST.get('medicines')
                medicines = json.loads(medicines_json) if medicines_json else []
                customer_obj = Customer.objects.get(id = contact_id)
                invoice = Invoice.objects.create(
                    customer=customer_obj,
                    payment_type= Payment_type
                )
                for medicine in medicines:
                    medicine_obj = Medicine.objects.get(id=medicine["id"])
                    if medicine_obj.quantity >= int(medicine["quantity"]):
                        InvoiceItem.objects.create(
                            invoice=invoice,
                            medicine=medicine_obj,
                            quantity=medicine["quantity"],
                            amount=medicine["amount"],
                            batch_id = medicine["batch"]
                        )
                        

                    else:
                        errors = "Out of Quantity"
                        return JsonResponse({'success': False, 'errors': errors}, status=400)
                invoice.grand_total = total_amount
                invoice.save()
            return redirect('dashboard:createinvoice')
                
        except Exception as e:
            print("error--------------", str(e))
            return render(request, 'dashboard/create_invoice.html', {'error_message': str(e)})
        
@method_decorator(login_required(login_url='/'), name='dispatch')
class ExportInvoiceView(View):

    def get(self, request, pk):
        user = request.user
        if pk == 'null':
            inv_obj = Invoice.objects.all().last()
            medicine_obj = InvoiceItem.objects.filter(invoice = inv_obj)
            context = {
                'user' : user,
                'inv_obj' : inv_obj,
                'medicine_obj' : medicine_obj
            }
            return render(request, 'dashboard/view_invoice.html', context)
        else:
            inv_obj = Invoice.objects.get(invoice_number=pk )
            medicine_obj = InvoiceItem.objects.filter(invoice = inv_obj)
            context = {
                'user' : user,
                'inv_obj' : inv_obj,
                'medicine_obj' : medicine_obj
            }
            return render(request, 'dashboard/view_invoice.html', context)

@login_required
def PrintInvoice(request, pk):
    user = request.user
    template_path = 'dashboard/print_invoice.html'
    inv_obj = Invoice.objects.get(invoice_number=pk )
    medicine_obj = InvoiceItem.objects.filter(invoice = inv_obj)
    context = {
        'user' : user,
        'inv_obj' : inv_obj,
        'medicine_obj' : medicine_obj
    }
    print_html = download_template(request,template_path, context )
    return print_html

        
        

        
from django.urls import path
from dashboard import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'dashboard'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('', views.LoginView.as_view(), name='login'),
    path('logout/',views.LogoutView.as_view(), name='logout_user'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('invoice/', views.InvoiceView.as_view(), name='invoice'),
    path('createinvoice/', views.CreateInvoiceView.as_view(), name='createinvoice'),
    path('exportinvoce/<str:pk>/', views.ExportInvoiceView.as_view(), name='exportinvoice'),
    path('printinvoice/<str:pk>/', views.PrintInvoice, name='printinvoice'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
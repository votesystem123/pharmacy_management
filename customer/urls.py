from django.urls import path
from customer import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'customer'

urlpatterns = [
    path('addcustomer/', views.AddCutomerView.as_view(), name='addcustomer'),
    path('customerlist/', views.CutomerListView.as_view(), name='customerlist'),
    path('editcustomer/<int:pk>/', views.EditCustomerView.as_view(), name='editcustomer'),
    path('listsupplier/', views.ListsupplierView.as_view(), name='listsupplier'),
    path('addsupplier/', views.AddSupplierView.as_view(), name='addsupplier'),
    path('listmedicine/', views.ListMedicineView.as_view(), name='listmedicine'),
    path('addmedicine/', views.PurchaseMedicineView.as_view(), name='addmedicine'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone
import uuid

# Create your models here.
ROLE_CHOICES = (
    ("user", "User"),
    ("admin", "Admin"),
)

class AiUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_admin = True
        user.role = "admin"
        user.is_staff = True
        user.save(using=self._db)
        return user

class AiUser(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True)
    role = models.CharField(max_length = 20, choices = ROLE_CHOICES, default = 'user')
    date_joined = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = AiUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
    class Meta:
        verbose_name = "Ai User"
        verbose_name_plural = "Ai Users"

PAYMENT_CHOICES = (
    ("cash", "Cash"),
    ("upi", "Upi"),
    ("card", "Card"),
)

class suppiler(models.Model):
    suppiler_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(null=True, unique=True)
    company_name = models.CharField(max_length=50)
    payment_type = models.CharField(max_length = 20, choices = PAYMENT_CHOICES, default = 'cash')
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.suppiler_name
    class Meta:
        verbose_name = "suppiler"
        verbose_name_plural = "suppiler"

class Medicine(models.Model):
    medicine_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(null=True)
    batch_id = models.CharField(max_length=50)
    exp_date = models.DateTimeField(null=True)
    suppiler_name = models.ForeignKey(suppiler, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.medicine_name
    class Meta:
        verbose_name = "medicine"
        verbose_name_plural = "medicine"

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(null=True, unique=True)
    dr_name = models.CharField(max_length=100)
    dr_dept = models.CharField(max_length=100)
    dr_hospital = models.CharField(max_length=100)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "customer"
        verbose_name_plural = "customer"

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=100, unique = True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length = 20, choices = PAYMENT_CHOICES, default = 'cash')
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date_created = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = 'Inv' + timezone.now().strftime('%Y%m%d') + '-' + str(uuid.uuid4().hex)[:3]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number
    
    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoice"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    batch_id = models.CharField(max_length=50)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Invoice: {self.invoice.invoice_number}, Medicine: {self.medicine.medicine_name}, Quantity: {self.quantity}"
    
    class Meta:
        verbose_name = "Invoice Items"
        verbose_name_plural = "Invoice Items"

@receiver(post_save, sender=InvoiceItem)
def decrease_quantity(sender, instance, created, **kwargs):
    if created:
        if instance.medicine.batch_id == instance.batch_id :
            instance.medicine.quantity -= int(instance.quantity)
            instance.medicine.save()

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    name = models.CharField(max_length=255, blank=True, default='')
    first_name=models.CharField(max_length=50,default='',null=True, blank=True)
    last_name=models.CharField(max_length=50,default='',null=True, blank=True)

    country=models.CharField(max_length=5,default='',null=True, blank=True)
    gender=models.CharField(max_length=5,choices=[("m", "m"),("f", "f")],default='m',null=True, blank=True)
    birth=models.DateField(default='2000-1-1',null=True, blank=True)
    photo=models.ImageField(upload_to='users/photos', default='users/photos/default.png',null=True)
    token=models.CharField(max_length=65,default='',null=True, blank=True)
    type=models.CharField(max_length=20,choices=[("doctor", "doctor"),("patient", "patient")], default='patient',null=True, blank=True)
    language=models.CharField(max_length=10,choices=[("en", "en"),("ar", "ar")], default='en',null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = '*Users'
    
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name or self.email.split('@')[0]

    
class Patient(User):
    
    def __str__(self):
        return str(self.email)
    
    class Meta:
        verbose_name = 'Patient'
        ordering = ['id']

class Doctor(User):
    specialization=models.CharField(max_length=50,default='',null=True, blank=True)
    clinic_address=models.CharField(max_length=50,default='',null=True, blank=True)
    rate=models.DecimalField(max_digits=2, decimal_places=1, default=0.0, null=True, blank=True)
    num_of_rate=models.DecimalField(max_digits=5, decimal_places=1, default=0.0, null=True, blank=True)
 
    def __str__(self):
        return str(self.email)
    
    class Meta:
        verbose_name = 'Doctor'
        ordering = ['id']
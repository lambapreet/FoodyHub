from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin 


class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, phone_number, password=None, role=2):
        if not email:
            raise ValueError("User must have an email")
        if not username:
            raise ValueError("User must have a username")
        
        user = self.model.objects.create(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            role=role
        )
        
        user.set_password(password)  
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, first_name, last_name, email, phone_number, password):
        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
            role=self.model.RESTAURANT  
        )
        
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True  
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    RESTAURANT = 1
    CUSTOMER = 2
    
    ROLE_CHOICE = (
        (RESTAURANT, 'Restaurant'),
        (CUSTOMER, 'Customer'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)  

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, default=CUSTOMER, blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)  
    last_login = models.DateTimeField(auto_now=True) 
    create_date = models.DateTimeField(auto_now_add=True)  
    modified_date = models.DateTimeField(auto_now=True)  

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # Users should be active by default
    is_superuser = models.BooleanField(default=False)  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):  
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users/profile_picture', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photo', blank=True, null=True)
    address_1 = models.CharField(max_length=50, blank=True, null=True)
    address_2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email if self.user else "Anonymous User"
    

from django.db import models
from rooms.models import Location
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.tokens import default_token_generator


class MyAccountManager(BaseUserManager):
    # overriding the create_user of the BaseUserManager
    def create_user(self, email, username, password=None, location=None):
        if not username:
            raise ValueError("The user must have a username.")
        if not email:
            raise ValueError("The user must have an email.")
        User = get_user_model()  # Get the custom user model
        user = User(
            username=username,
            email=self.normalize_email(email),
            location=location,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, location=None):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            location=location,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    ORG_TYPE_CHOICES = [
        ("Restaurants", "Restaurants"),
        ("Fast Food", "Fast Food"),
        ("Coffee", "Coffee"),
        ("Hotel", "Hotel"),
        ("School", "School"),
        ("Medical", "Medical"),
        ("Pharmacy", "Pharmacy"),
        ("Culture", "Culture"),
        ("Corporate", "Corporate"),
        ("Non Profit", "Non Profit"),
        ("Individual", "Individual"),
        ("Religious", "Religious"),
        ("Business", "Business"),
        ("Embassy", "Embassy"),
        ("Night Life", "Night Life"),
    ]
    username = models.CharField(max_length=30, unique=True)
    organization_name = models.CharField(verbose_name="Organization name", max_length=60)
    email = models.EmailField(verbose_name="Email", max_length=60, unique=True)
    type_of_organization = models.CharField(max_length=30, choices=ORG_TYPE_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1)
    password = models.CharField(verbose_name="Password", max_length=300)
    confirm_password = models.CharField(verbose_name="Confirm Password", max_length=30)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)
    objects = MyAccountManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class PasswordResetToken(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate_token(cls, user):
        token = default_token_generator.make_token(user)
        cls.objects.create(user=user, token=token)
        return token

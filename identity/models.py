from django.db import models
from rooms.models import Location
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission



# Create a user
# Create a superuser
class MyAccountManager(BaseUserManager):
   
    # overriding the create_user of the BaseUserManager
    def create_user(self, email, username, password=None, location=None):
        if not username:
            raise ValueError("The user must have a username.")
        if not email:
            raise ValueError("The user must have an email.")
        User = get_user_model()  # Get the custom user model
        user =User(
            username=username,
            email=self.normalize_email(email),
            location=location,
        )
        user.set_password(password)
        user.save(using=self._db)
        # Assign the user to the Manager-admins group
        # try:
        #     group = Group.objects.get(name='Manager-admins')
        #     print(group)
        # except Group.DoesNotExist:
        #     # Handle the case when the group doesn't exist
        #     raise ValueError("The specified group does not exist.")
        
        # user.groups.add(group)
        
       
        '''
            For adding custom permissions after creating them do:
            
            permission = Permission.objects.get(codename='your_permission_codename')  # Replace 'your_permission_codename' with the actual permission codename
            user.user_permissions.add(permission)
        
        '''
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

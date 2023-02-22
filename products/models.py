from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """manager for user profiles"""

    def create_user(self, email, name, password=None):
        """create a new user profile"""
        if not email:
            raise ValueError("User must choose Email Address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    # we need super user to have password
    def create_superuser(self, email, name, password):
        """create and save a new super user with given details"""
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """database model for users in the system """
    email = models.EmailField(max_length=225, unique=True)
    name = models.CharField(max_length=255)
    is_activate = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """retrieve short name of user"""
        return self.name

    def __str__(self):
        """return string represent of our user"""
        return self.email


class Product(models.Model):
    """database model for products in the system"""
    name = models.CharField(max_length=60)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Cart(models.Model):
    """Handling the cart model"""

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name


class CartItem(models.Model):
    """Handling cart items"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='items')
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cartitems')
    quantity=models.IntegerField(default=0)


    def __str__(self):
        return self.product.name
    
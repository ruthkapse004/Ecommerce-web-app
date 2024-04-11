from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=256)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self) -> str:
        return self.user.get_full_name()

    def name(self):
        return str(self)

    def email(self):
        return self.user.email

    class Meta:
        ordering = ['id', 'user__first_name', 'user__last_name']


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=256, null=False)
    city = models.CharField(max_length=256, null=False)
    state = models.CharField(max_length=256, null=False)
    zipcode = models.CharField(max_length=10, null=False)
    shipping_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(F"{self.address}, {self.city}, {self.state}, {self.zipcode}")


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['id', 'title']


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="products",
                              default="/products/placeholder.png")

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        ordering = ['id', 'name']

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Order(models.Model):
    transaction_id = models.CharField(max_length=256, null=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.SET_NULL, null=True)
    order_date = models.DateTimeField(auto_now=True)
    order_amount = models.DecimalField(
        max_digits=8, decimal_places=2, default=0)
    complete = models.BooleanField(default=False)

    @property
    def get_order_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_order_items(self):
        order_items = self.orderitem_set.all()
        total_items = sum([item.quantity for item in order_items])
        return total_items


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.product)

    @property
    def get_total(self):
        return self.product.price * self.quantity

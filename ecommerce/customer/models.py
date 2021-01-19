from django.db import models
from django.contrib.auth.models import User
from product.models import Products
#Each customer
class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=300,null=True,blank=True)
    contactNo=models.DecimalField(max_digits=10,decimal_places=0,null=True,blank=True)
    address=models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.name

#Orders by customers
class Order(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    orderedDate=models.DateTimeField(auto_now_add=True)
    delivered=models.BooleanField(default=False)

    class Meta:
        ordering=['-orderedDate']

    def __str__(self):
        return str(self.customer)+"  "+str(self.orderedDate)

#Products in each order
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity=models.DecimalField(max_digits=5,decimal_places=0)

    def __str__(self):
        return str(self.order.customer.name)+" "+str(self.quantity)+"x"+str(self.product)

#Cart of each customer
class CartItem(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.DO_NOTHING)
    product=models.ForeignKey(Products,on_delete=models.DO_NOTHING)
    quantity=models.DecimalField(max_digits=5,decimal_places=0)

    def __str__(self):
        return str(self.customer.name)+" "+str(self.quantity)+"x"+str(self.product)
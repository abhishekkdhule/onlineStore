from django.db import models

# Create your models here.
class Products(models.Model):
    name=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=4,decimal_places=1)
    unit=models.CharField(max_length=10)
    image=models.ImageField(upload_to='product/static/images/',blank=True,null=True)

    def __str__(self):
        return self.name
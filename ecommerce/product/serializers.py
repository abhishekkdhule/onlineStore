from rest_framework import serializers
from . models import Products

class ProductSerailizer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields=['name','price','unit','image']
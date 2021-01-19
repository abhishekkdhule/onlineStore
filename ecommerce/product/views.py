import json
import requests
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Products
from customer.models import Customer,Order,OrderItem,CartItem
from . serializers import ProductSerailizer
from rest_framework.response import Response
from rest_framework.decorators import api_view


#API for products
@api_view(['GET','POST'])
def ProductList(request):
    products=Products.objects.all()
    serailisedData=ProductSerailizer(products,many=True)
    print("api call")
    return Response(serailisedData.data)

#Homepage displaying products
def HomePage(request):
    res=requests.get('http://localhost:8000/api/products')
    products= (res.json())

    return render(request,'product/index.html',{'products':products})


#Cart of a customer
def cart(request):
    customerCart=[]
    customer = Customer.objects.get(user=request.user)
    total=0
    try:                            #checking if cart is empty or not
        cartOfUser=CartItem.objects.filter(customer=customer)
        for i in cartOfUser:
            item={
                'name':i.product.name,
                'quantity':i.quantity,
                'price':i.quantity*i.product.price,
            }
            total+=(i.quantity*i.product.price)
            customerCart.append(item)
    except CartItem.DoesNotExist:
        pass
    return render(request,'product/cart.html',{"customerCart":customerCart,"total":total})

#Add Item to cart
def addItem(request):
    data=json.loads(request.body)
    print(data['product'])
    customer = Customer.objects.get(user=request.user)
    product=Products.objects.get(name=data['product'])
    price=product.price
    quantity=1
    try:                            #checking if cart is empty or not
        cartOfUser=CartItem.objects.get(customer=customer,product=product)
        cartOfUser.quantity+=1       #if cart already has that particular product then just update the quantity
        quantity=cartOfUser.quantity
        cartOfUser.save()
    except CartItem.DoesNotExist:
        obj=CartItem(customer=customer,product=product,quantity=1)  #if the product is not present in the cutomers cart then add that item to cart and set quantity to 1
        obj.save()
    return JsonResponse({"price":price,'quantity':quantity})


#Delete Item from cart
def deleteItem(request):
    data=json.loads(request.body)
    print(data['product'])
    customer = Customer.objects.get(user=request.user)
    product=Products.objects.get(name=data['product'])
    price=product.price
    quantity=0
    try:                            #checking if cart is empty or not
        cartOfUser=CartItem.objects.get(customer=customer,product=product)
        if(cartOfUser.quantity==1): #If only one quantity of that particular product exists then delete the object
            cartOfUser.delete()
        else:
            cartOfUser.quantity-=1   
            quantity=cartOfUser.quantity   
            cartOfUser.save()
    except CartItem.DoesNotExist:
        pass
    return JsonResponse({"price":price,'quantity':quantity})


#Place and order and add records to orders
def placeOrder(request):
    customer = Customer.objects.get(user=request.user)
    if(customer.address=="" or customer.email=="" or customer.contactNo==None):
        return JsonResponse({"order":"notplaced"})
    else:
        try:                            #checking if cart is empty or not
            cartOfUser=CartItem.objects.filter(customer=customer)
            if(len(cartOfUser)!=0):
                order=Order(customer=customer)
                order.save()
                for i in cartOfUser:
                    obj=OrderItem(order=order,product=i.product,quantity=i.quantity)
                    obj.save()
                cartOfUser.delete()  
            else:
                return JsonResponse({"order":"emptycart"}) 
        except CartItem.DoesNotExist:
            pass
        print("ordered placed")
        return JsonResponse({"order":"placed"})



# Rendering profile of of every customer
def profile(request):
    customer=Customer.objects.get(user=request.user)
    prof={'name':customer.name,'email':customer.email,'contact':customer.contactNo,'address':customer.address}
    orders=Order.objects.filter(customer=customer)

    ords=[]
    # orderitems=OrderItem.objects.filter(order=orders)
    for order in orders:
        odr={}
        listOfItems=[]
        total=0
        odr['date']=order.orderedDate
        odr['id']="collapse"+str(order.id)
        orderitems=OrderItem.objects.filter(order=order)
        
        for item in orderitems:
            items={}
            items['name']=item.product.name
            items['quantity']=item.quantity
            items['price']=item.product.price
            total=total+(item.quantity*item.product.price)
            listOfItems.append(items)
        odr["orderItems"]=listOfItems
        odr['total']=total
        ords.append(odr)
    return render(request,'product/profile.html',{'profile':prof,'orders':ords})



# Updation of user profile    
def updateProfile(request):
    name=request.POST['nameUpdate']
    email=request.POST['emailUpdate']
    contact=request.POST['contactUpdate']
    address=request.POST['addressUpdate']
    customer=Customer.objects.get(user=request.user)
    customer.name=name
    customer.email=email
    customer.contactNo=contact
    customer.address=address
    print(len(contact))
    try:
        if(len(contact)==10):
            customer.clean_fields()
            customer.save()
        else:
            messages.info(request,"Invalid credentials!!!")
    except ValidationError as e:
        messages.info(request,e)
    print(name,email,contact,address)
    return redirect('profile')
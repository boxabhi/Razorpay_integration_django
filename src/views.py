from django.shortcuts import render
import razorpay
from django.views.decorators.csrf import csrf_exempt

from .models import Coffee
import json
def home(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = int(request.POST.get('amount')) * 100
        client = razorpay.Client(auth =("rzp_test_fIQJWiEsCEUyzS" , "UiKtan5P5LpnMFLNkKvCEw7x"))
        payment = client.order.create({'amount':amount, 'currency':'INR',
                              'payment_capture':'1' })
        
        coffee = Coffee(name = name , amount =amount , order_id = payment['id'])
        coffee.save()
        
        return render(request, 'index.html' ,{'payment':payment})
    return render(request, 'index.html')


@csrf_exempt
def success(request):
    if request.method == "POST":
        a =  (request.POST)
        order_id = ""
        for key , val in a.items():
            if key == "razorpay_order_id":
                order_id = val
                break
    
        user = Coffee.objects.filter(order_id = order_id).first()
        user.paid = True
        user.save()
        

    return render(request, "success.html")
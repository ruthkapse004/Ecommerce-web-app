from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
import json
from datetime import datetime
from .models import Product, Order, OrderItem, ShippingAddress
from .utils import process_order, authenticated_user


def store(request: HttpRequest):
    products = Product.objects.all()
    order_data = process_order(request)
    context = {'products': products, 'order': order_data['order']}
    # print("request: ", request)

    return render(request, 'store/store.html', context)


def cart(request: HttpRequest):
    order_data = process_order(request)
    context = {'items': order_data['items'], 'order': order_data['order']}

    return render(request, 'store/cart.html', context)


@login_required(login_url="signin")
def order_summary(request: HttpRequest):
    items, order = authenticated_user(request)
    # print(order_data['items'])
    context = {'items': items, 'order': order}

    return render(request, 'store/order_summary.html', context)


@login_required(login_url="signin")
def update_cart_item(request: HttpRequest):
    data = json.loads(request.body)
    product_id = data["productId"]
    action = data["action"]
    # print(f"Action: {action} Product Id: {product_id}")

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order = Order.objects.get(customer=customer, complete=False)
    orderitem, _ = OrderItem.objects.get_or_create(
        order=order, product=product)

    response = ""
    if action == "add":
        orderitem.quantity += 1
        response = "Item added"
    elif action == "remove":
        orderitem.quantity -= 1
        response = "Item removed"
    orderitem.save()

    if orderitem.quantity == 0 or action == "delete":
        response = "Item Deleted"
        orderitem.delete()

    return JsonResponse(response, safe=False)


@login_required(login_url="signin")
def place_order(request: HttpRequest):
    transaction_id = str(datetime.now().timestamp())
    data = json.loads(request.body)
    print(transaction_id, "DATA: ", data)

    with transaction.atomic():
        customer = request.user.customer
        order = Order.objects.get(customer=customer, complete=False)
        order.transaction_id = transaction_id
        order.order_amount = order.get_order_total
        order.complete = True
        order.save()

        ShippingAddress.objects.create(
            customer=customer, order=order,
            address=data['formShippingData']['address'],
            city=data['formShippingData']['city'],
            state=data['formShippingData']['state'],
            zipcode=data['formShippingData']['zipcode'],
        )
        response = "Your order has been placed successfully."

    return JsonResponse(response, safe=False)

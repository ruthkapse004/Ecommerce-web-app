# This file just stores the utility functions to do repeated tasks.

from .models import Product, Order
import json


def unauthenticated_user(request):
    # stores no of items in cart
    items_count = 0
    # stores total of all prices of items in the cart
    items_total = 0
    items = []

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    # Here cart.keys() gives list of product_ids which are strings, but in SQL queries product ids are int.
    # It's somehow converting ids to int, So if it's working don't touch it. or we could simply map ids to int.
    products = list(Product.objects.filter(pk__in=cart.keys()))
    n = len(products)

    # If some products are deleted from DB for any reason, but still present in cart cookie, then iterating over cart will throw errors.
    # Hence, we are directly iterating over products which we receive from DB.
    for product in products:
        key = str(product.id)
        total = product.price * cart[key]['quantity']
        items_count += cart[key]['quantity']
        items_total += total

        items.append({
            "product": product,
            "quantity": cart[key]['quantity'],
            "get_total": total,
        })

    # print(F"CART: {cart} \nTotal Items: {item_count}")
    order = {'get_order_items': items_count, 'get_order_total': items_total, }

    return (items, order)


def authenticated_user(request):
    customer = request.user.customer
    order, _ = Order.objects.prefetch_related(
        'orderitem_set__product').get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()

    return (items, order)


def process_order(request):
    if request.user.is_authenticated:
        items, order = authenticated_user(request)
    else:
        items, order = unauthenticated_user(request)

    return {'items': items, 'order': order}

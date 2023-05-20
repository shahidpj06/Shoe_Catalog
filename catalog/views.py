from django.shortcuts import render
from django.views.generic import ListView
from .models import Product, Cart


class ProductList(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'index.html'


def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    quantity = int(request.POST.get('quantity', 0))
    gift_wrapped = bool(request.POST.get('gift_wrapped', False))

    cart_item = Cart(product=product, quantity=quantity, gift_wrapped=gift_wrapped)
    cart_item.save()

    return render(request, 'cart.html', {'cart_item': cart_item})


def checkout(request):
    if request.method == 'POST':
        quantities = {
            'product_a': int(request.POST.get('product_a_quantity', 0)),
            'product_b': int(request.POST.get('product_b_quantity', 0)),
            'product_c': int(request.POST.get('product_c_quantity', 0))
        }
        gift_wraps = {
            'product_a': request.POST.get('product_a_gift_wrap', False),
            'product_b': request.POST.get('product_b_gift_wrap', False),
            'product_c': request.POST.get('product_c_gift_wrap', False)
        }

        cart_total = 0
        discount_name = ''
        discount_amount = 0
        shipping_fee = 0
        gift_wrap_fee = 0

        for product in Product.objects.all():
            quantity = quantities[product.name.lower()]
            cart_total += quantity * product.price

            if quantity > 10:
                discount_name = 'bulk_5_discount'
                discount_amount = 0.05 * quantity * product.price

            if sum(quantities.values()) > 20:
                discount_name = 'bulk_10_discount'
                discount_amount = 0.1 * cart_total

            if sum(quantities.values()) > 30 and quantity > 15:
                discount_name = 'tiered_50_discount'
                discount_amount = 0.5 * (quantity - 15) * product.price

            if discount_name == '':
                if cart_total > 200:
                    discount_name = 'flat_10_discount'
                    discount_amount = 10

            if gift_wraps[product.name.lower()]:
                gift_wrap_fee += quantity

        shipping_fee = (sum(quantities.values()) // 10) * 5

        subtotal = cart_total
        total = subtotal - discount_amount + gift_wrap_fee + shipping_fee

        return render(request, 'checkout.html', {
            'quantities': quantities,
            'products': Product.objects.all(),
            'subtotal': subtotal,
            'discount_name': discount_name,
            'discount_amount': discount_amount,
            'shipping_fee': shipping_fee,
            'gift_wrap_fee': gift_wrap_fee,
            'total': total
        })

    return render(request, 'checkout.html', {'products': Product.objects.all()})

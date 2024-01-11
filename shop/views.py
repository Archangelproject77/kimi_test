from django.shortcuts import render, get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone

from .forms import CartAddProductForm, CouponApplyForm, OrderCreateForm
from .models import Category, Product, OrderItem, Coupon
from .cart.cart import Cart



def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {'category': category, 'categories': categories, 'products': products}
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    carousel = product.get_carousel()
    print("\n\n#----------------Carousel ------------", carousel, '\n\n#----------------------------"', product.image.url)
    context = {'product': product, 'categories': categories, 'cart_product_form': cart_product_form, 'carousel': carousel}
    return render(request, 'shop/product/detail.html', context)

#--------------------------------------------------------cart-----------------------------------------
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})
    coupon_apply_form = CouponApplyForm()
    return render(request, 'shop/cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form})

#-------------------------------------------------------------order-----------------------------------------------------

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
            # clear the cart
            cart.clear()
            return render(request, 'shop/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'shop/order/create.html', {'cart': cart, 'form': form})

#---------------------------------------------------------------coupons-----------------------------------------------

@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')

#-----------------------------------------------------------------------------------

def home(request):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    context = {'category': category, 'categories': categories, 'products': products}
    return render(request,'shop/home.html',context=context)

def about(request):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    context = {'category': category, 'categories': categories, 'products': products}
    return render(request,'shop/about.html',context=context)



def contact(request):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    context = {'category': category, 'categories': categories, 'products': products}
    return render(request,'shop/contact.html',context=context)
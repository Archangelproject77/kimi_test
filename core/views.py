from django.shortcuts import render

from shop.models import Category, Product
from blog.models import Post

# Create your views here.

def home(request):
    #shop
    category = None
    categories = Category.objects.all()
    products = list(Product.objects.filter(available=True))[:4]
    
    #blog
    post = list(Post.objects.all())[:3]
    
    context = {'category': category, 'categories': categories, 'products': products, 'posts': post}
    return render(request,'core/index.html',context=context)


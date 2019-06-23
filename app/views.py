from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Product, Review
from .forms import ReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()


    context = {
        'product_list': products,
    }

    return render(request, template, context)


def product_view(request, pk):
    request.session['has_commented'] = False
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)
    review_list = []
    reviews = product.review.all()
    for review in reviews:
        review_list.append(review.text)



    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
           review = Review(text = form.cleaned_data['text'], product = product)
           review.save()
           reviews = product.review.all()
           for review in reviews:
               review_list.append(review.text)
           request.session['has_commented'] = True
    else:
        form = ReviewForm()
       # логика для добавления отзыва


    context = {
        'form': form,
        'product': product,
        'reviews': review_list,
        'is_review_exist': request.session['has_commented']}

    return render(request, template, context)

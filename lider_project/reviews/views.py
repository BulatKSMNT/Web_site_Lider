from django.shortcuts import render, redirect
from django.urls import reverse

from reviews.forms import ReviewForm
from reviews.models import Review


def add_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index') + '#reviews')
    else:
        form = ReviewForm()

    return render(request, "reviews/add_review.html", {"form": form})


def reviews_list(request):
    reviews = Review.objects.all()
    return render(request, "core/index.html", {"reviews": reviews})

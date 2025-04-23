from django.shortcuts import render, get_object_or_404

def catalog_list(request):
    return render(request, 'catalog/catalog_list.html')
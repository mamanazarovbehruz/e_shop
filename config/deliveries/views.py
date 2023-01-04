from django.shortcuts import render

# Create your views here.

def deli(request):
    return render(request, 'detail.html')
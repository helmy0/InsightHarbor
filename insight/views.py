from django.shortcuts import render, redirect
from .forms import InsightRequest

from django.core.files.storage import FileSystemStorage

def home(request):
    if request.method == 'POST':
        print("Successeded")
        image = request.FILES['image']
        fs = FileSystemStorage(location='static/imgs/')
        filename = fs.save(image.name, image)
        return redirect('result')  # redirect to the result view
    return render(request, "home.html")


def result(request):
    context = {}


    return render(request, "result.html", context)
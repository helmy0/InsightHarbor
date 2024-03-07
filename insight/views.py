from django.shortcuts import render
from .forms import InsightRequest
# Create your views here.


def home(request):
    context = {}
    form = InsightRequest()



    context = {
        'form': form,
    }

    return render(request, "home.html", context)
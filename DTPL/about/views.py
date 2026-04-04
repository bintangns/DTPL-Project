from django.shortcuts import render

# Create your views here.

def ecotourism(request):
    return render(request, 'about/ecotourism.html')
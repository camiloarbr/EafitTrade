from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html', {'name': 'Camilo Arbelaez'})

def about(request):
    return render(request, 'about.html')   

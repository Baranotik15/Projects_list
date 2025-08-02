from django.shortcuts import render

# Create your views here.

def wheel_of_fortune(request):
    return render(request, 'wheel_of_fortune/wheel_of_fortune_main_page.html')

from django.shortcuts import render


def wheel_of_fortune(request):
    return render(request, 'wheel_of_fortune/wheel_of_fortune_main_page.html')

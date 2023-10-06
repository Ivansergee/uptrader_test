from django.shortcuts import render


def show_menu(response):
    return render(response, 'menu/index.html')

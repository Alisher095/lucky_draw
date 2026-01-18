from django.shortcuts import render

def index(request):
    """
    Renders the landing page at templates/index.html
    """
    return render(request, 'index.html')

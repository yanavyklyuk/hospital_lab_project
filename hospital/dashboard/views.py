from django.shortcuts import render


def create_dashboard(request):
    return render(request, 'dashboard/dash.html')


def create_bokeh_dashboard(request):
    return render(request, 'dashboard/dash2.html')
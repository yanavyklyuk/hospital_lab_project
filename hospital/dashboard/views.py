from django.shortcuts import render

def create_dashboard(request):
    return render(request, 'dashboard/dash.html')
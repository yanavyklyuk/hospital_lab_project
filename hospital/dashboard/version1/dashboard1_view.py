from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'dashboard/dashboard_v1_template.html')
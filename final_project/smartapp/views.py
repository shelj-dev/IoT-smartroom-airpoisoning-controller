import json
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData, Limit
from .forms import limitForm
from datetime import datetime


SAFE_LIMIT = 4000


@csrf_exempt
def receive_sensor_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            value = data.get("value")

            print("Sensor Value:", value)

            if value is None:
                return JsonResponse({"error": "No value received"}, status=400)

            SensorData.objects.create(value=value)

            return JsonResponse({"status": "success"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST required"})



def update_threshold(request):
    data = Limit.objects.first() 

    if request.method == 'POST':
        form = limitForm(request.POST , instance=data)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:        
        form = limitForm(instance=data)
        return render(request, 'update_threshold.html'  , {'form': form})
    



def home(request):

    latest = SensorData.objects.last()
    
    if latest:
        latest.is_safe = latest.value <= SAFE_LIMIT

    return render(request, "home.html", {
        "latest": latest,
        "page": "home"
    })

 

def graph(request):
    history = SensorData.objects.order_by('-timestamp')
    return render(request, "graph.html", {"history": history,"page": "graph"})



def logs(request):
    history = SensorData.objects.order_by('-timestamp')

    month = request.GET.get('month')

    if not month:
        month = datetime.now().month   

    history = history.filter(timestamp__month=month)

    history = history[:50]

    for r in history:
        r.is_safe = r.value <= SAFE_LIMIT

    return render(request, "logs.html", {
        "history": history,
        "selected_month": int(month),
        "page": "logs"
    })
def about(request):
    return render(request, "about.html", {"page": "about"})

def help_page(request):
    return render(request, "help.html", {"page": "help"})
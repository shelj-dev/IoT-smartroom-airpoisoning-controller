import json
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData, Limit
from .forms import limitForm


SAFE_LIMIT = 300


@csrf_exempt
def receive_sensor_data(request):

    if request.method == "POST":

        data = json.loads(request.body)

        value = float(data.get("value", 0))

        print("Sensor Value:", value)

        SensorData.objects.create(value=value)
        
        return JsonResponse({
            "status": "saved",
            "value": value,
        })

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
    
def dashboard(request):

    latest = SensorData.objects.last()
    history = SensorData.objects.order_by('-timestamp')[:10]

    return render(request, "dashboard.html", {
        "latest": latest,
        "history": history
    })
import json
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData, Limit
from .forms import limitForm


SAFE_LIMIT = 3500


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
            return redirect('dashboard')
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



def dashboard(request):

    latest = SensorData.objects.last()
    history = SensorData.objects.order_by('-timestamp')[:10]

    # Add safety logic manually
    if latest:
        latest.is_safe = latest.value <= SAFE_LIMIT

    for r in history:
        r.is_safe = r.value <= SAFE_LIMIT

    return render(request, "dashboard.html", {
        "latest": latest,
        "history": history
    })
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GasReading


SAFE_LIMIT = 300


@csrf_exempt
def receive_sensor_data(request):

    if request.method == "POST":

        data = json.loads(request.body)

        value = float(data.get("value", 0))

        print("Sensor Value:", value)

        safe = value < SAFE_LIMIT

        GasReading.objects.create(
            gas_type="COMBUSTIBLE_GAS",
            value=value,
            is_safe=safe
        )

        return JsonResponse({
            "status": "saved",
            "value": value,
            "safe": safe
        })

    return JsonResponse({"error": "POST required"})


def dashboard(request):

    latest = GasReading.objects.order_by('-timestamp').first()
    history = GasReading.objects.order_by('-timestamp')[:20]

    return render(request, "dashboard.html", {
        "latest": latest,
        "history": history
    })
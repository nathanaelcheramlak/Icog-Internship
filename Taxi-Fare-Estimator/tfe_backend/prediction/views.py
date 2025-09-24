import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import generate_random_ride, predict_fare_from_model

@csrf_exempt
def populate_db(request):
    """
    POST /prediction/populate/
    Body: { "count": 10 }
    """
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            count = int(body.get("count", 1))
        except Exception:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        trips = [generate_random_ride() for _ in range(count)]
        return JsonResponse({"message": f"{len(trips)} trips added."})

    return JsonResponse({"error": "POST request required"}, status=405)


@csrf_exempt
def predict_fare(request):
    """
    POST /prediction/predict/
    Body: { "distance": 5, "time": 15, "day_of_week": 3, "passengers": 2}
    """
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
        except Exception:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        required = ["distance", "time", "day_of_week", "passengers"]
        if not all(k in body for k in required):
            return JsonResponse({"error": f"Missing fields {required}"}, status=400)

        predicted_fare = predict_fare_from_model(body)
        return JsonResponse({"predicted_fare": predicted_fare})

    return JsonResponse({"error": "POST request required"}, status=405)

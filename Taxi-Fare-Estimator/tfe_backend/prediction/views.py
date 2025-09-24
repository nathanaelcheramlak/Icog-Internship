import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .utils import generate_random_ride, predict_fare_from_model
import numpy as np
import pandas as pd
from .models import TaxiFare
from .ml_model import TaxiFareEstimator

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
    Body: { "distance": 5, "time": 15, "day_of_week": 3, "passengers": 2 }
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

        # Ensure it's a native Python float
        if isinstance(predicted_fare, (np.generic,)):  
            predicted_fare = predicted_fare.item()
        else:
            predicted_fare = float(predicted_fare)

        return JsonResponse({"predicted_fare": round(predicted_fare, 2)})

    return JsonResponse({"error": "POST request required"}, status=405)

@csrf_exempt
def train_model(request):
    """
    GET/POST /prediction/train/
    Trains the ML model on all TaxiFare records and saves it.
    Returns basic metrics if training succeeds.
    """
    if request.method not in ["GET", "POST"]:
        return JsonResponse({"error": "GET or POST request required"}, status=405)

    # Fetch all records
    all_fares_qs = TaxiFare.objects.all().values()
    if not all_fares_qs:
        for _ in range(200):
            generate_random_ride()
        all_fares_qs = TaxiFare.objects.all().values()

    df = pd.DataFrame(list(all_fares_qs))
    if df.empty:
        return JsonResponse({"error": "No data available to train."}, status=400)

    estimator = TaxiFareEstimator()
    estimator.train(df)

    # compute metrics on the training data
    try:
        metrics = estimator.evaluate(df)
    except Exception:
        metrics = None

    response = {"message": "Model trained and saved successfully."}
    if metrics:
        response["metrics"] = {k: float(v) for k, v in metrics.items()}
    response["num_records"] = int(len(df))

    return JsonResponse(response)


def ui_index(request):
    return render(request, "prediction/index.html")
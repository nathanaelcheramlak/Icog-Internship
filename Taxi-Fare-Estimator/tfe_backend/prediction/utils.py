import random
import pandas as pd
from .models import TaxiFare
from .ml_model import TaxiFareEstimator

def generate_random_ride():
    """
    Generate one synthetic taxi ride record with random values
    and save it into the database.
    """

    # Random features
    distance = round(random.uniform(1, 30), 2)        
    time = random.randint(0, 23)                 
    day_of_week = random.randint(0, 6)                  
    passengers = random.randint(1, 4)                   

    base_fare = 3.0
    per_km_rate = random.uniform(1.5, 2.5)

    surge = 5 if (time >= 18 or time <= 6) else 0

    # Weekend multiplier 
    weekend_multiplier = 1.2 if day_of_week in [5, 6] else 1.0

    # Final fare
    fare = (base_fare + distance * per_km_rate + passengers * 0.5 + surge) * weekend_multiplier
    fare += random.gauss(0, 2)   # add random noise
    fare = round(max(fare, 3.0), 2)   # ensure >= base fare

    # Save to DB
    ride = TaxiFare.objects.create(
        distance=distance,
        time=time,
        day_of_week=day_of_week,
        passengers=passengers,
        fare=fare,
    )

    return ride

def predict_fare_from_model(features: dict) -> float:
    """
    Predict fare using the trained ML model.
    """
    estimator = TaxiFareEstimator()
    try:
        estimator.load_model()
    except FileNotFoundError:
        # Train and save the model if it doesn't exist
        all_fares = TaxiFare.objects.all().values()
        if not all_fares:
            # If there's no data generate 
            for _ in range(100):
                generate_random_ride()
            all_fares = TaxiFare.objects.all().values()
        
        df = pd.DataFrame(list(all_fares))
        estimator.train(df)
        estimator.save_model()

    return estimator.predict(features)

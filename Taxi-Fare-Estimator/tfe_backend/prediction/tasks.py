from celery import shared_task
from datetime import datetime, timedelta
import pandas as pd
from .models import TaxiFare
from .ml_model import TaxiFareEstimator

@shared_task
def retrain_model():
    """
    Celery task to retrain the model with data from the past 24 hours.
    """
    # Calculate the time 24 hours ago
    time_threshold = datetime.now() - timedelta(hours=24)

    # Fetch new data from the last 24 hours
    new_data = TaxiFare.objects.filter(created_at__gte=time_threshold)

    if new_data.exists():
        # Convert queryset to DataFrame
        df = pd.DataFrame(list(new_data.values()))

        # Instantiate the estimator and retrain
        estimator = TaxiFareEstimator()
        estimator.train(df)

        print(f"Model retrained with {len(df)} new records.")
    else:
        print("No new data for retraining.")

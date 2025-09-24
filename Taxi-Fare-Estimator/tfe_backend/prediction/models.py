from django.db import models

class TaxiFare(models.Model):
    distance = models.FloatField()           # in kilometers
    time = models.IntegerField(db_index=True)             # hour of day (0–23)
    day_of_week = models.IntegerField(db_index=True)      # 0=Mon ... 6=Sun
    passengers = models.IntegerField()       # passengers count
    fare = models.FloatField()               # target 

    created_at = models.DateTimeField(auto_now_add=True) 


    def __str__(self):
        return f"Ride: {self.distance} km, {self.passengers} pax, fare ${self.fare}"

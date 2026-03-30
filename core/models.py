from django.db import models
from django.contrib.auth.models import User


class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    land_area = models.FloatField(help_text='Land area in acres', default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.district}"


class CropAdvisory(models.Model):
    SEASON_CHOICES = [
        ('kharif', 'Kharif (June-Nov)'),
        ('rabi', 'Rabi (Nov-April)'),
        ('zaid', 'Zaid (March-June)'),
    ]

    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advisories')

    # Soil inputs
    nitrogen = models.FloatField(help_text='N content in soil (kg/ha)')
    phosphorus = models.FloatField(help_text='P content in soil (kg/ha)')
    potassium = models.FloatField(help_text='K content in soil (kg/ha)')
    ph_value = models.FloatField(help_text='Soil pH (0-14)')
    rainfall = models.FloatField(help_text='Average rainfall in mm')
    temperature = models.FloatField(help_text='Average temperature in Celsius')
    humidity = models.FloatField(help_text='Humidity percentage')
    season = models.CharField(max_length=20, choices=SEASON_CHOICES, default='kharif')

    # AI Outputs
    recommended_crop = models.CharField(max_length=100)
    confidence_score = models.FloatField(default=0.0)
    top_3_crops = models.JSONField(default=list)

    # AI Feature 2: Predicted yield
    predicted_yield = models.FloatField(null=True, blank=True, help_text='Predicted yield in kg/acre')
    yield_category = models.CharField(max_length=20, default='medium')  # low/medium/high

    # AI Feature 3: Fertilizer suggestion
    fertilizer_suggestion = models.TextField(blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.farmer.username} - {self.recommended_crop} ({self.created_at.date()})"


class WeatherData(models.Model):
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    month = models.IntegerField()
    avg_temperature = models.FloatField()
    avg_rainfall = models.FloatField()
    avg_humidity = models.FloatField()

    class Meta:
        unique_together = ['state', 'district', 'month']

    def __str__(self):
        return f"{self.district} - Month {self.month}"

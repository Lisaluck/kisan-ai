from django.contrib import admin
from .models import FarmerProfile, CropAdvisory, WeatherData


@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'state', 'district', 'land_area', 'created_at']
    search_fields = ['user__username', 'district', 'state']


@admin.register(CropAdvisory)
class CropAdvisoryAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'recommended_crop', 'confidence_score', 'predicted_yield', 'season', 'created_at']
    list_filter  = ['recommended_crop', 'season', 'yield_category']
    search_fields = ['farmer__username', 'recommended_crop']
    readonly_fields = ['recommended_crop', 'confidence_score', 'top_3_crops', 'predicted_yield', 'fertilizer_suggestion']


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['state', 'district', 'month', 'avg_temperature', 'avg_rainfall']

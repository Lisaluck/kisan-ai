from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from ai.crop_ai import get_crop_recommender, get_yield_predictor, get_fertilizer_advisor
from .models import CropAdvisory, FarmerProfile


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        state = request.POST.get('state', '')
        district = request.POST.get('district', '')
        land_area = request.POST.get('land_area', 1.0)

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'core/register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        FarmerProfile.objects.create(
            user=user,
            state=state,
            district=district,
            land_area=float(land_area)
        )
        login(request, user)
        messages.success(request, 'Welcome! Your account has been created.')
        return redirect('dashboard')

    return render(request, 'core/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    advisories = CropAdvisory.objects.filter(farmer=request.user)[:5]
    total = CropAdvisory.objects.filter(farmer=request.user).count()

    # Stats for dashboard cards
    crop_counts = {}
    for a in CropAdvisory.objects.filter(farmer=request.user):
        crop_counts[a.recommended_crop] = crop_counts.get(a.recommended_crop, 0) + 1
    top_crop = max(crop_counts, key=crop_counts.get) if crop_counts else 'N/A'

    try:
        profile = request.user.farmerprofile
    except Exception:
        profile = None

    return render(request, 'core/dashboard.html', {
        'advisories': advisories,
        'total': total,
        'top_crop': top_crop,
        'profile': profile,
    })


@login_required
def get_advisory(request):
    if request.method == 'POST':
        try:
            N = float(request.POST['nitrogen'])
            P = float(request.POST['phosphorus'])
            K = float(request.POST['potassium'])
            ph = float(request.POST['ph_value'])
            rainfall = float(request.POST['rainfall'])
            temperature = float(request.POST['temperature'])
            humidity = float(request.POST['humidity'])
            season = request.POST.get('season', 'kharif')

            # AI 1: Crop Recommendation
            recommender = get_crop_recommender()
            crop, confidence, top3 = recommender.predict(N, P, K, ph, rainfall, temperature, humidity)

            # AI 2: Yield Prediction
            predictor = get_yield_predictor()
            yield_val, yield_cat = predictor.predict(N, P, K, ph, rainfall, temperature, humidity)

            # AI 3: Fertilizer Suggestion
            advisor = get_fertilizer_advisor()
            fertilizer = advisor.suggest(crop, N, P, K)

            # Save to DB
            advisory = CropAdvisory.objects.create(
                farmer=request.user,
                nitrogen=N, phosphorus=P, potassium=K,
                ph_value=ph, rainfall=rainfall,
                temperature=temperature, humidity=humidity,
                season=season,
                recommended_crop=crop,
                confidence_score=confidence,
                top_3_crops=top3,
                predicted_yield=yield_val,
                yield_category=yield_cat,
                fertilizer_suggestion=fertilizer,
            )

            return redirect('result', pk=advisory.pk)

        except (ValueError, KeyError) as e:
            messages.error(request, f'Invalid input: {str(e)}')

    return render(request, 'core/get_advisory.html')


@login_required
def result_view(request, pk):
    advisory = get_object_or_404(CropAdvisory, pk=pk, farmer=request.user)
    return render(request, 'core/result.html', {'advisory': advisory})


@login_required
def history(request):
    advisories = CropAdvisory.objects.filter(farmer=request.user)
    return render(request, 'core/history.html', {'advisories': advisories})


@login_required
def api_predict(request):
    """AJAX endpoint for live prediction preview"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            N = float(data['nitrogen'])
            P = float(data['phosphorus'])
            K = float(data['potassium'])
            ph = float(data['ph_value'])
            rainfall = float(data['rainfall'])
            temperature = float(data['temperature'])
            humidity = float(data['humidity'])

            recommender = get_crop_recommender()
            crop, confidence, top3 = recommender.predict(N, P, K, ph, rainfall, temperature, humidity)

            predictor = get_yield_predictor()
            yield_val, yield_cat = predictor.predict(N, P, K, ph, rainfall, temperature, humidity)

            return JsonResponse({
                'crop': crop,
                'confidence': confidence,
                'top3': top3,
                'yield': yield_val,
                'yield_category': yield_cat,
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST only'}, status=405)

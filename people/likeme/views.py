from django.http import JsonResponse
import pandas as pd
import numpy as np
from pathlib import Path

csvPath = Path('./data.csv')
data = pd.read_csv(csvPath)

# Create your views here.

def index(request):
    params = request.GET
    return JsonResponse({'peopleLikeYou': []})

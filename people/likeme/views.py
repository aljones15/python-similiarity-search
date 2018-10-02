from django.http import JsonResponse
import pandas as pd
import numpy as np
from pathlib import Path
from .transform import byName

csvPath = Path('./data.csv')
df = pd.read_csv(csvPath)

# Create your views here.

def index(request):
    df.loc[:, 'score'] = 0
    params = request.GET
    if 'name' in params:
        byName(df, params['name'])

    return JsonResponse({'peopleLikeYou': []})

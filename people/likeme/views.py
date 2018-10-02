from django.http import JsonResponse
import pandas as pd
import numpy as np
from pathlib import Path
from .transform import byName, topTen

def getDataFrame():
    csvPath = Path('./data.csv')
    df = pd.read_csv(csvPath)
    df.loc[:, 'score'] = 0
    return df

# Create your views here.

def index(request):
    df = getDataFrame()
    params = request.GET
    if 'name' in params:
        byName(df, params['name'])
    results = topTen(df)
    return JsonResponse({'peopleLikeYou': results})

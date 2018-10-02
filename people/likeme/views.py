import sys
from django.http import JsonResponse
import pandas as pd
import numpy as np
from pathlib import Path
from .transform import byName, topTen, byExperience

def getDataFrame():
    csvPath = Path('./data.csv')
    df = pd.read_csv(csvPath)
    df.loc[:, 'score'] = 0
    return df

# Create your views here.

def index(request):
    try:
        df = getDataFrame()
        params = request.GET

        if 'name' in params:
            byName(df, params['name'])

        if 'experienced' in params:
            byExperience(df, params['experienced'])

        results = topTen(df)
        return JsonResponse({'peopleLikeYou': results})

    except KeyError as e:
        response = JsonResponse({'error': 'Unsupported Key'})
        response.status_code = 400;
        return response

    except:
        e = sys.exc_info()[0]
        print(e)
        response = JsonResponse({'error': 'Unknown'})
        response.status_code = 400;
        return response


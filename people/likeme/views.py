import sys
from django.http import JsonResponse
import pandas as pd
import numpy as np
from pathlib import Path
from .transform import byName, topTen, byExperience, byEudlidianDistance, bySingleLocation

def getDataFrame():
    "gets the data frame and sets the score to 0"
    # move to models
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
        fulldistance = 'latitude' in params and 'longitude' in params
        if fulldistance:
            byEudlidianDistance(df, params['latitude'], params['longitude'])
        elif 'latitude' in params:
            bySingleLocation(df, 'latitude', params['latitude'])
        elif 'longitude' in params:
            bySingleLocation(df, 'longitude', params['longitude'])

        results = topTen(df)
        return JsonResponse({'peopleLikeYou': results})

    except KeyError as e:
        response = JsonResponse({'error': 'Unsupported Key'})
        response.status_code = 400;
        return response

    except:
        e = sys.exc_info()[0]
        raise e
        response = JsonResponse({'error': 'Unknown: ' + e.message})
        response.status_code = 400;
        return response


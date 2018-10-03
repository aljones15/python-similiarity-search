import sys
from django.http import JsonResponse
import pandas as pd
import numpy as np
from pathlib import Path
from .transform import by_name, top_ten, by_experience, by_distance

def getDataFrame():
    "gets the data frame and sets the score to 0"
    # move to models
    csv_path = Path('./data.csv')
    data_frame = pd.read_csv(csv_path)
    data_frame.loc[:, 'score'] = 0
    return data_frame

# Create your views here.

def index(request):
    "the index handler for the route people-like-me"
    try:
        data_frame = getDataFrame()
        params = request.GET
        score_count = 0

        if 'name' in params:
            name_scores = by_name(data_frame, params['name'])
            data_frame['score'] += name_scores
            score_count += 1

        if 'experienced' in params:
            exp_scores = by_experience(data_frame, params['experienced'])
            data_frame['score'] += exp_scores
            score_count += 1

        if 'latitude' in params:
            new_scores = by_distance(data_frame, 'latitude', float(params['latitude']))
            data_frame['score'] += new_scores
            score_count += 1

        if 'longitude' in params:
            new_scores = by_distance(data_frame, 'longitude', float(params['longitude']))
            data_frame['score'] += new_scores
            score_count += 1

        if 'age' in params:
            new_scores = by_distance(data_frame, 'age', int(params['age']))
            data_frame['score'] += new_scores
            score_count += 1

        if any(param in params for param in ('monthly income', 'monthlyIncome')):
            income = params['monthlyIncome'] if 'monthlyIncome' in params else params['monthly income']
            new_scores = by_distance(data_frame, 'monthly income', int(income))
            data_frame['score'] += new_scores
            score_count += 1

        if score_count > 0:
            data_frame['score'] = data_frame['score'] / score_count

        results = top_ten(data_frame)
        return JsonResponse({'peopleLikeYou': results})

    except KeyError:
        response = JsonResponse({'error': 'Unsupported Key'})
        response.status_code = 400
        return response

    except:
        "this should be logged here but do not have a logger"
        e = sys.exc_info()[0]
        response = JsonResponse({'error': 'Unknown Error'})
        response.status_code = 400
        return response

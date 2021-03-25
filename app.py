import numpy as np
import pandas as pd
import pickle

from flask import Flask, request, jsonify, render_template
from waitress import serve

app = Flask(__name__)

# read and prepare model 
pred = pd.read_csv('predictions.csv')
rank = pd.read_csv('rangering_cleaned.csv')
movie = pd.read_csv('film_cleaned.csv')
@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/predict', methods=['POST'])
def predict():
    ''' 
    Rendering results on HTML
    '''
    # get data
    features = dict(request.form)    

    # sjekk input
    if features['user_id'] not in pred.columns:
        return render_template('./index.html',
                               prediction_text='This userid is not in our database :)')
    # predict
    uid = features['user_id']
    uidpred = pred[[uid,'FilmID']]
    recommendations = movie[['Tittel','FilmID']].merge(uidpred[~uidpred.FilmID.isin(rank[rank.BrukerID == uid].FilmID)].sort_values(uid).tail(10),left_on = 'FilmID',right_on = 'FilmID').Tittel.values

    # prepare output
    return render_template('./index.html',
                           prediction_text="The top 10 recommended movies for userid {}".format(
                               uid,
                               ),
                               movie_1 = recommendations[0],
                               movie_2 = recommendations[1],
                               movie_3 = recommendations[2],
                               movie_4 = recommendations[3],
                               movie_5 = recommendations[4],
                               movie_6 = recommendations[5],
                               movie_7 = recommendations[6],
                               movie_8 = recommendations[7],
                               movie_9 = recommendations[8],
                               movie_10 = recommendations[9],
                               )

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)

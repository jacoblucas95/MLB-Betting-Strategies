from flask import jsonify,request, render_template
from datetime import datetime, date
from pprint import pprint
import numpy as np
import pandas as pd

from .run import app
from flask_app import Filter, create_betting_results, create_betting_results_test, home, visitor, overs, underdogs, unders, favorites, df, test_df, home_underdogs_ml, visitor_favorites_ml, visitor_underdogs_ml, visitor_underdogs_rl, home_favorites_ml, home_favorites_rl, longshot_ml, longshot_ou, longshot_rl
# from app.game_filter import date_range


@app.route('/test',  methods=['GET'])
def test():
	if request.method == 'GET':
		df = test_df.to_json(orient='records')
		print(test_df.info())
		return jsonify(df)

@app.route('/api/dataset',  methods=['GET','POST'])
def get_dataset():
	if request.method == 'GET':
		df = Filter(1270354000,1554610000).date_range_df()
		return jsonify(create_betting_results('ou', favorites, 100, df))
	elif request.method == 'POST':
		sd = float(request.json['start_date'])
		ed = float(request.json['end_date'])


		df = Filter(sd, ed).date_range_df()
		return jsonify(create_betting_results('ou', favorites, 100, df))





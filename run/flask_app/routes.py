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
		df = Filter(date(2018,1,1),date.today()).date_range_df()
		return jsonify(create_betting_results_test('ou', longshot_ou, 100, df))
			
	elif request.method == 'POST':
		sd = request.json['start_date']
		ed = request.json['end_date']
		start_date = datetime.fromtimestamp(sd)
		end_date = datetime.fromtimestamp(ed)

		s = start_date.strftime('%Y-%m-%d')
		sy = int(s[0:4])
		sm = int(s[5:7])
		sd = int(s[8:10])

		e = end_date.strftime('%Y-%m-%d')
		ey = int(e[0:4])
		em = int(e[5:7])
		ed = int(e[8:10])

		df = Filter(date(sy,sm,sd), date(ey,em,ed)).date_range_df()
		return jsonify(create_betting_results('ou', favorites, 100, df))





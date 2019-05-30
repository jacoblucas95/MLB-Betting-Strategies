from flask import jsonify,request, render_template
from datetime import datetime, date
from pprint import pprint
import numpy as np
import pandas as pd

from .run import app
from flask_app import Filter, create_betting_results, create_betting_results_test, home, visitor, overs, underdogs, unders, favorites, home_underdogs_ml, visitor_favorites_ml, visitor_underdogs_ml, visitor_underdogs_rl, home_favorites_ml, home_favorites_rl, longshot_teams_ml, longshot_teams_rl
# from app.game_filter import date_range

@app.route('/api/dataset',  methods=['GET','POST'])
def get_dataset():
	if request.method == 'GET':
		sd = 1554523200
		ed = 1554609600
		df = Filter(sd,ed).date_range_df()
		return jsonify(create_betting_results('ml', favorites, 100, df))

	elif request.method == 'POST':
		sd = int(request.json['start_date'])
		ed = int(request.json['end_date'])
		df = Filter(sd, ed).date_range_df()
		return jsonify(create_betting_results('ou', underdogs, 100, df))





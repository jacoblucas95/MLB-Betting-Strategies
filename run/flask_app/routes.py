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
		bet_type = request.json['bet_type']
		strategy_dict = {'home': home, 'visitor': visitor, 'overs': overs, 
				'underdogs': underdogs, 'unders': unders, 'favorites': favorites, 
				'home_underdogs_ml': home_underdogs_ml, 'visitor_favorites_ml': visitor_favorites_ml, 
				'visitor_underdogs_ml': visitor_underdogs_ml, 'visitor_underdogs_rl': visitor_underdogs_rl, 
				'home_favorites_ml': home_favorites_ml, 'home_favorites_rl': home_favorites_rl, 
				'longshot_teams_ml': longshot_teams_ml, 'longshot_teams_rl': longshot_teams_rl}
		strat = request.json['strategy']
		strategy = strategy_dict[strat]
		bet_amount = request.json['bet_amount']
		return jsonify(create_betting_results(bet_type, strategy, bet_amount, df))

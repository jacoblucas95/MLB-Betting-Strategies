from flask import jsonify,request, render_template
from datetime import datetime, date
from pprint import pprint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

from .run import app
from flask_app import create_betting_results, home_team, visitor_team, overs, underdogs, unders, favorites, test_df
from flask_app.game_filter import Filter
# from app.game_filter import date_range


@app.route('/')
def root():
	return jsonify({
		"game_1":{
			"home_team":"Home Team1",
			"away_team":"Away Team1",
			"location":"City1",
			"date":"1499817600",
			"final_score":"69",
			"odds":"6:9",
			"open_close_ratio":"9:6",
			"pitcher":{
				"name":"Mikey Mike",
				"hand":"R"
				}
		},
		"game_2":{
			"home_team":"Home Team2",
			"away_team":"Away Team2",
			"location":"City2",
			"date":"1531353600",
			"final_score":"420",
			"odds":"4:20",
			"open_close_ratio":"4:20",
			"pitcher":{
				"name":"Bobby Bob",
				"hand":"L"
				}
		}
	})

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
		return jsonify(create_betting_results('ou', favorites, 100, df))
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


# @app.route('/test/graph', methods=['GET'])
# def test_graph():
# 	if request.method == 'GET':
# 		data = create_betting_results('ml', favorites, 100, df=test_df)
# 		data = pd.DataFrame(data)
# 		fig = plt.figure()
# 		ax = plt.axes()
# 		x = data['date']
# 		y = data['count']
# 		graph = ax.plot(kind='line', x=x, y=y, color='red')
# 		graph.savefig('/Baseball/plot.png')
# 		return render_template('plot_test.html')
		

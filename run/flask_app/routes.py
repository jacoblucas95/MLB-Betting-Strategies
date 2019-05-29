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


@app.route('/test',  methods=['GET'])
def test():
	if request.method == 'GET':
		df = test_df.to_json(orient='records')
		print(test_df.info())
		return jsonify(df)

@app.route('/api/dataset',  methods=['GET','POST'])
def get_dataset():
	if request.method == 'GET':
		df = Filter(1554523000,1554610000).date_range_df()
		return jsonify(create_betting_results('ou', favorites, 100, df))
	elif request.method == 'POST':
		sd = float(request.json['start_date'])
		ed = float(request.json['end_date'])


		df = Filter(sd, ed).date_range_df()
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
		

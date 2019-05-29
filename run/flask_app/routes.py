from flask import jsonify,request, render_template
from datetime import datetime, date
from pprint import pprint
import numpy as np
import pandas as pd

from .run import app
from flask_app import Filter, create_betting_results, create_betting_results_test, home, visitor, overs, underdogs, unders, favorites, home_underdogs_ml
from .game_filter import Filter


@app.route('/test',  methods=['GET'])
def test():
	if request.method == 'GET':
		df = test_df.to_json(orient='records')
		print(test_df.info())
		return jsonify(df)

@app.route('/api/dataset',  methods=['GET','POST'])
def get_dataset():
	if request.method == 'GET':
		sd = 1554523200
		ed = 1554609600
		df = Filter(sd, ed).date_range_df()
		return jsonify(create_betting_results('ou', overs, 100, df))

	elif request.method == 'POST':
		sd = int(request.json['start_date'])
		ed = int(request.json['end_date'])
		df = Filter(sd, ed).date_range_df()
		return jsonify(create_betting_results('ou', underdogs, 100, df))


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


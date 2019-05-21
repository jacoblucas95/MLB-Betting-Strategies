
from flask import jsonify,request
from .run import app
from app import game


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

@app.route('/api/dataset',  methods=['GET','POST'])
def get_dataset():
	if request.method == 'GET':
		return jsonify(game.create_games_generator())

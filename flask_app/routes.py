#!/usr/bin/env python3

from flask import Flask,jsonify,request

app = Flask(__name__)

@app.route('/')
def root():
	return jsonify({"status":"API Works"})

@app.route('/api/dataset', methods=['GET','POST'])
def get_dataset():
	if request.method == 'GET':
		return jsonify({})


if __name__ == '__main__':
	app.run(debug=True)

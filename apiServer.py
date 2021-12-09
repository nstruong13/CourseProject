from flask import Flask, make_response, jsonify, request, send_file
# from ScrapeMineViz import get_visualizations

app = Flask(__name__)

@app.route('/query', methods=['GET'])

def query():
	inputQuery = request.args.get('query')
	response = make_response(jsonify({"html": get_visualizations(inputQuery)}))
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@app.route('/getHeatMapImage', methods=['GET'])
def getHeatMapImage():
	response = make_response(send_file("heatmap.png", mimetype='image/png'))
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@app.route('/test', methods=['GET'])
def test():
	response = make_response("test successful");
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=105)
